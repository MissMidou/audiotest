const MANIFEST_URL = "./manifest.json";
const LOAD_TIMEOUT_MS = 15000;

const statusMessage = document.getElementById("statusMessage");
const listSection = document.getElementById("listSection");
const playerSection = document.getElementById("playerSection");
const audioList = document.getElementById("audioList");
const audioPlayer = document.getElementById("audioPlayer");
const nowPlaying = document.getElementById("nowPlaying");
const trackError = document.getElementById("trackError");
const environmentHint = document.getElementById("environmentHint");

let activeButton = null;

function setStatus(text, type = "loading") {
  statusMessage.classList.remove("hidden", "loading", "error");
  statusMessage.classList.add(type);
  statusMessage.textContent = text;
}

function hideStatus() {
  statusMessage.classList.add("hidden");
}

function showTrackError(message) {
  trackError.textContent = message;
  trackError.classList.remove("hidden");
}

function clearTrackError() {
  trackError.textContent = "";
  trackError.classList.add("hidden");
}

function isWeChatBrowser() {
  return /MicroMessenger/i.test(navigator.userAgent || "");
}

function fetchWithTimeout(url, timeoutMs) {
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), timeoutMs);
  return fetch(url, { signal: controller.signal }).finally(() => {
    clearTimeout(timer);
  });
}

function setActiveButton(button) {
  if (activeButton) {
    activeButton.classList.remove("active");
  }
  activeButton = button;
  if (activeButton) {
    activeButton.classList.add("active");
  }
}

function playTrack(item, button) {
  clearTrackError();
  setActiveButton(button);
  nowPlaying.textContent = `正在播放: ${item.label}`;
  audioPlayer.src = item.url;
  audioPlayer
    .play()
    .catch(() => showTrackError(`无法播放「${item.label}」，请稍后重试。`));
}

function renderList(items) {
  audioList.innerHTML = "";
  items.forEach((item) => {
    const li = document.createElement("li");
    const button = document.createElement("button");
    button.type = "button";
    button.textContent = item.label;
    button.addEventListener("click", () => playTrack(item, button));
    li.appendChild(button);
    audioList.appendChild(li);
  });
}

async function init() {
  if (!isWeChatBrowser()) {
    environmentHint.textContent = "提示：当前不是微信内置浏览器，请优先使用微信扫码访问。";
  }

  setStatus("加载中...");

  let payload;
  try {
    const response = await fetchWithTimeout(MANIFEST_URL, LOAD_TIMEOUT_MS);
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }
    payload = await response.json();
  } catch (error) {
    setStatus("加载失败，请检查网络后重试。", "error");
    return;
  }

  const items = Array.isArray(payload.items) ? payload.items : [];
  if (items.length === 0) {
    setStatus("暂无可播放音频。", "error");
    return;
  }

  renderList(items);
  listSection.classList.remove("hidden");
  playerSection.classList.remove("hidden");
  hideStatus();
}

audioPlayer.addEventListener("error", () => {
  showTrackError("音频加载失败，请尝试切换其他曲目。");
});

init();
