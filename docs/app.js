/* ============================================
   CatHideOuts — App Script
   ============================================ */

// ──────────────────────────────────────────────
//  設定: GitHub の情報をここに入力
// ──────────────────────────────────────────────
const CONFIG = {
    githubUser: 'gomi-kuzu',
    githubRepo: 'cat-hideouts',
};

// ──────────────────────────────────────────────
//  カテゴリ定義
// ──────────────────────────────────────────────
const CATEGORIES = {
    battle:     '⚔️ バトル',
    adventure:  '🗺️ 冒険・フィールド',
    calm:       '🌿 穏やか・日常',
    sad:        '🌧️ 悲しみ・切なさ',
    tension:    '💀 緊張・ホラー',
    happy:      '✨ 喜び・勝利',
    mysterious: '🔮 神秘・幻想',
};

// ──────────────────────────────────────────────
//  トラックデータ
//  曲を追加するときはこの配列に追加するだけ！
// ──────────────────────────────────────────────
const TRACKS = [
    // --- サンプルデータ（実際の曲ができたら差し替えてください）---
    {
        id: '001_fuan01',
        title: '不安１',
        category: 'sad',
        fileName: '001_fuan01.wav',  // GitHub Releaseにアップするファイル名（リリースタグはファイル名から自動生成）
    },
    {
        id: '002_tansaku01',
        title: '探索１',
        category: 'adventure',
        fileName: '002_tansaku01.wav',
    },
    {
        id: '003_tansaku02',
        title: '探索２',
        category: 'calm',
        fileName: '003_tansaku02.wav',
    },
    {
        id: '004_kyouki01',
        title: '狂気１',
        category: 'battle',
        fileName: '004_kyouki01.wav',
    },
    {
        id: '005_relax01',
        title: 'リラックス１',
        category: 'calm',
        fileName: '005_relax01.wav',
    },
    {
        id: '006_kansatsu01',
        title: '観察１',
        category: 'adventure',
        fileName: '006_kansatsu01.wav',
    },
    {
        id: '007_happiness01',
        title: 'ハピネス１',
        category: 'happy',
        fileName: '007_happiness01.wav',
    },
    {
        id: '008_fanfare01',
        title: 'ファンファーレ１',
        category: 'happy',
        fileName: '008_fanfare01.wav',
    },
    {
        id: '009_gekko01',
        title: '月光１',
        category: 'mysterious',
        fileName: '009_gekko01.wav',
    },
    {
        id: `010_hushinkan01`,
        title: '不信感１',
        category: 'tension',
        fileName: '010_hushinkan01.wav',
    },
    {
        id: `011_gimon01`,
        title: '疑問１',
        category: 'tension',
        fileName: '011_gimon01.wav',
    },
    {
        id: `012_dasaku01`,
        title: '駄作１',
        category: 'battle',
        fileName: '012_dasaku01.wav',
    },
    {
        id: `013_bouken01`,
        title: '冒険１',
        category: 'adventure',
        fileName: '013_bouken01.wav',
    },
    {
        id: `014_madoromi01`,
        title: '微睡１',
        category: 'mysterious',
        fileName: '014_madoromi01.wav',
    },
    {
        id: `015_yoake01`,
        title: '夜明け１',
        category: 'mysterious',
        fileName: '015_yoake01.wav',
    },
    {
        id: `016_dasaku02`,
        title: '駄作２',
        category: 'battle',
        fileName: '016_dasaku02.wav',
    },
    {
        id: `017_hazure01`,
        title: 'はずれ１',
        category: 'sad',
        fileName: '017_hazure01.wav',
    },
    {
        id: `018_shingun01`,
        title: '進軍１',
        category: 'adventure',
        fileName: '018_shingun01.wav',
    },
    {
        id: `019_osyaberi01`,
        title: 'おしゃべり１',
        category: 'calm',
        fileName: '019_osyaberi01.wav',
    },
    {
        id: `020_fuan02`,
        title: '不安２',
        category: 'sad',
        fileName: '020_fuan02.wav',
    },
    {
        id: `021_kokoromi01`,
        title: '試み１',
        category: 'happy',
        fileName: '021_kokoromi01.wav',
    },
        {
        id: `022_happiness02`,
        title: 'ハピネス２',
        category: 'happy',
        fileName: '022_happiness02.wav',
    },
    {
        id: `023_kokoromi02`,
        title: '試み２',
        category: 'happy',
        fileName: '023_kokoromi02.wav',
    },
    {
        id: `024_gimon02`,
        title: '疑問２',
        category: 'tension',
        fileName: '024_gimon02.wav',
    },
        {
        id: `025_fuon01`,
        title: '不穏１',
        category: 'tension',
        fileName: '025_fuon01.wav',
    },
        {
        id: `026_hibi01`,
        title: '日々１',
        category: 'calm',
        fileName: '026_hibi01.wav',
    },
        {
        id: `027_hatsuratsu01`,
        title: '溌溂１',
        category: 'happy',
        fileName: '027_hatsuratsu01.wav',
    },
        {
        id: `028_tansaku03`,
        title: '探索３',
        category: 'adventure',
        fileName: '028_tansaku03.wav',
    },
        {
        id: `029_bouken02`,
        title: '冒険２',
        category: 'adventure',
        fileName: '029_bouken02.wav',
    },
        {
        id: `030_sabaku01`,
        title: '砂漠１',
        category: 'adventure',
        fileName: '030_sabaku01.wav',
    },
        {
        id: `031_dasaku03`,
        title: '駄作３',
        category: 'mysterious',
        fileName: '031_dasaku03.wav',
    },
        {
        id: `032_taiji01`,
        title: '対峙１',
        category: 'battle',
        fileName: '032_taiji01.wav',
    },
        {
        id: `033_kyouran01`,
        title: '狂乱１',
        category: 'tension',
        fileName: '033_kyouran01.wav',
    },
        {
        id: `034_noujiru01`,
        title: '脳汁１',
        category: 'happy',
        fileName: '034_noujiru01.wav',
    },
];

// ──────────────────────────────────────────────
//  ソート・日付の状態
// ──────────────────────────────────────────────
let currentCategory = 'all';
let sortOrder = 'desc'; // 'desc' = 新しい順, 'asc' = 古い順

// dateMap は localStorage からリストア（初期表示から NEW! を出すため）
const DATE_MAP_KEY = 'cathideouts_dateMap';
const dateMap = (() => {
    try {
        return JSON.parse(localStorage.getItem(DATE_MAP_KEY)) || {};
    } catch {
        return {};
    }
})();

// ──────────────────────────────────────────────
//  ダウンロードURL生成
//  リリースタグはファイル名（拡張子なし）と同じ
// ──────────────────────────────────────────────
function getDownloadUrl(track) {
    const releaseTag = track.fileName.replace(/\.[^.]+$/, ''); // 拡張子を除去
    return `https://github.com/${CONFIG.githubUser}/${CONFIG.githubRepo}/releases/download/${releaseTag}/${track.fileName}`;
}

// ──────────────────────────────────────────────
//  日付フォーマット（YYYY/MM/DD）
// ──────────────────────────────────────────────
function formatDate(isoString) {
    if (!isoString) return null;
    const d = new Date(isoString);
    const y = d.getFullYear();
    const m = String(d.getMonth() + 1).padStart(2, '0');
    const day = String(d.getDate()).padStart(2, '0');
    return `${y}/${m}/${day}`;
}

// ──────────────────────────────────────────────
//  トラックカードHTML生成
// ──────────────────────────────────────────────
function createTrackCard(track, index) {
    const downloadUrl = getDownloadUrl(track);
    const uploadDate = formatDate(dateMap[track.fileName]);
    const isNew = (() => {
        const d = dateMap[track.fileName];
        if (!d) return false;
        return (Date.now() - new Date(d).getTime()) < 3 * 24 * 60 * 60 * 1000;
    })();

    const card = document.createElement('div');
    card.className = 'track-card';
    card.dataset.category = track.category;
    card.style.animationDelay = `${index * 0.08}s`;

    card.innerHTML = `
        <div class="track-header">
            <h3 class="track-title">${track.title}${isNew ? ' <span class="badge-new">NEW!</span>' : ''}</h3>
            <span class="track-category-badge">${CATEGORIES[track.category] || track.category}</span>
        </div>
        <div class="track-player">
            <audio controls preload="none" id="audio-${track.id}">
                <source src="${downloadUrl}" type="audio/mpeg">
            </audio>
        </div>
        <div class="track-controls">
            <button class="btn btn-sm btn-loop" data-track-id="${track.id}" title="ループ再生">
                🔄 ループ再生
            </button>
        </div>
        <div class="track-actions">
            <div class="track-info">
                <span class="download-count" id="count-${track.id}">📥 集計中...</span>
                <span class="track-date">${uploadDate ? `📅 ${uploadDate}` : ''}</span>
            </div>
            <a href="${downloadUrl}" class="btn btn-sm btn-download" download>
                ⬇ ダウンロード
            </a>
        </div>
    `;

    // ループボタンのイベントリスナーを追加
    const loopBtn = card.querySelector('.btn-loop');
    const audio = card.querySelector('audio');
    
    loopBtn.addEventListener('click', () => {
        audio.loop = !audio.loop;
        loopBtn.classList.toggle('active', audio.loop);
        loopBtn.title = audio.loop ? 'ループ再生: ON' : 'ループ再生: OFF';
    });

    return card;
}

// ──────────────────────────────────────────────
//  トラック一覧の描画
// ──────────────────────────────────────────────
function renderTracks(category = 'all') {
    currentCategory = category;
    const grid = document.getElementById('trackGrid');
    const emptyState = document.getElementById('emptyState');
    grid.innerHTML = '';

    let filtered = category === 'all'
        ? [...TRACKS]
        : TRACKS.filter(t => t.category === category);

    // 日付順ソート（dateMap が空の場合は元の順序を維持）
    filtered.sort((a, b) => {
        const dateA = dateMap[a.fileName] ? new Date(dateMap[a.fileName]).getTime() : 0;
        const dateB = dateMap[b.fileName] ? new Date(dateMap[b.fileName]).getTime() : 0;
        return sortOrder === 'desc' ? dateB - dateA : dateA - dateB;
    });

    if (filtered.length === 0) {
        emptyState.style.display = 'block';
    } else {
        emptyState.style.display = 'none';
        filtered.forEach((track, i) => {
            grid.appendChild(createTrackCard(track, i));
        });
    }
}

// ──────────────────────────────────────────────
//  カテゴリフィルター
// ──────────────────────────────────────────────
function initCategoryFilter() {
    const buttons = document.querySelectorAll('.filter-btn');

    buttons.forEach(btn => {
        btn.addEventListener('click', () => {
            // アクティブ切り替え
            buttons.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');

            const category = btn.dataset.category;
            renderTracks(category);
        });
    });
}

// ──────────────────────────────────────────────
//  GitHub API でダウンロード数取得
// ──────────────────────────────────────────────
async function fetchDownloadCounts() {
    try {
        // GitHub API はデフォルトで 30 件までしか返さないため、ページングで全件取得
        const perPage = 100;
        let page = 1;
        let releases = [];

        while (true) {
            const apiUrl = `https://api.github.com/repos/${CONFIG.githubUser}/${CONFIG.githubRepo}/releases?per_page=${perPage}&page=${page}`;
            const response = await fetch(apiUrl);

            if (!response.ok) {
                console.warn('GitHub API レスポンスエラー:', response.status);
                setAllCountsTo('—');
                return;
            }

            const batch = await response.json();
            if (!Array.isArray(batch) || batch.length === 0) {
                break;
            }

            releases = releases.concat(batch);

            if (batch.length < perPage) {
                break;
            }
            page += 1;
        }

        // ファイル名 → ダウンロード数・アップロード日のマップを作成
        const countMap = {};
        releases.forEach(release => {
            release.assets.forEach(asset => {
                // 同じファイル名が複数リリースにある場合は合算
                if (countMap[asset.name]) {
                    countMap[asset.name] += asset.download_count;
                } else {
                    countMap[asset.name] = asset.download_count;
                }
                // アップロード日は最も古い日付を採用
                if (!dateMap[asset.name] || asset.created_at < dateMap[asset.name]) {
                    dateMap[asset.name] = asset.created_at;
                }
            });
        });

        // dateMap をキャッシュとして保存
        try { localStorage.setItem(DATE_MAP_KEY, JSON.stringify(dateMap)); } catch {}

        // 日付情報が揃ったので再描画（ソート・日付表示に反映）
        renderTracks(currentCategory);

        // 各トラックのカウントを更新
        let totalDownloads = 0;
        TRACKS.forEach(track => {
            const el = document.getElementById(`count-${track.id}`);
            if (el) {
                const count = countMap[track.fileName];
                if (count !== undefined) {
                    totalDownloads += count;
                    el.textContent = `📥 ${count.toLocaleString()} DL`;
                } else {
                    el.textContent = '📥 — DL';
                }
            }
        });

        // トータルダウンロード数を表示
        const totalEl = document.getElementById('totalDownloads');
        if (totalEl) {
            totalEl.textContent = totalDownloads > 0 ? totalDownloads.toLocaleString() : '0';
        }

    } catch (error) {
        console.error('GitHub API 取得エラー:', error);
        setAllCountsTo('—');
        const totalEl = document.getElementById('totalDownloads');
        if (totalEl) {
            totalEl.textContent = '—';
        }
    }
}

function setAllCountsTo(value) {
    TRACKS.forEach(track => {
        const el = document.getElementById(`count-${track.id}`);
        if (el) {
            el.textContent = `📥 ${value} DL`;
        }
    });
    const totalEl = document.getElementById('totalDownloads');
    if (totalEl) {
        totalEl.textContent = value;
    }
}

// ──────────────────────────────────────────────
//  モバイルメニュー
// ──────────────────────────────────────────────
function initMobileMenu() {
    const btn = document.querySelector('.mobile-menu-btn');
    const nav = document.querySelector('.global-nav');

    if (btn && nav) {
        btn.addEventListener('click', () => {
            nav.classList.toggle('open');
        });

        // ナビリンクをクリックしたら閉じる
        nav.querySelectorAll('a').forEach(link => {
            link.addEventListener('click', () => {
                nav.classList.remove('open');
            });
        });
    }
}

// ──────────────────────────────────────────────
//  ヘッダーのスクロール効果
// ──────────────────────────────────────────────
function initScrollEffect() {
    const header = document.querySelector('.site-header');

    window.addEventListener('scroll', () => {
        if (window.scrollY > 50) {
            header.style.borderBottomColor = 'rgba(192, 132, 252, 0.15)';
        } else {
            header.style.borderBottomColor = '';
        }
    });
}

// ──────────────────────────────────────────────
//  ソートトグル
// ──────────────────────────────────────────────
function initSortToggle() {
    const btn = document.getElementById('sortToggle');
    if (!btn) return;

    function updateButton() {
        const label = btn.querySelector('.sort-label');
        const arrow = btn.querySelector('.sort-arrow');
        if (sortOrder === 'desc') {
            label.textContent = '新しい順';
            arrow.textContent = '▼';
        } else {
            label.textContent = '古い順';
            arrow.textContent = '▲';
        }
    }

    btn.addEventListener('click', () => {
        sortOrder = sortOrder === 'desc' ? 'asc' : 'desc';
        updateButton();
        renderTracks(currentCategory);
    });
}

// ──────────────────────────────────────────────
//  初期化
// ──────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
    renderTracks();
    initCategoryFilter();
    initSortToggle();
    initMobileMenu();
    initScrollEffect();
    fetchDownloadCounts();
});
