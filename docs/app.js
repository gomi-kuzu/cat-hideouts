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
    // {
    //     id: 'bgm_happy_01',
    //     title: '歓喜のファンファーレ',
    //     category: 'happy',
    //     fileName: 'bgm_happy_01.mp3',
    // },
    // {
    //     id: 'bgm_mysterious_01',
    //     title: '星降る聖域',
    //     category: 'mysterious',
    //     fileName: 'bgm_mysterious_01.mp3',
    // },
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
    const apiUrl = `https://api.github.com/repos/${CONFIG.githubUser}/${CONFIG.githubRepo}/releases`;

    try {
        const response = await fetch(apiUrl);

        if (!response.ok) {
            console.warn('GitHub API レスポンスエラー:', response.status);
            setAllCountsTo('—');
            return;
        }

        const releases = await response.json();

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
        TRACKS.forEach(track => {
            const el = document.getElementById(`count-${track.id}`);
            if (el) {
                const count = countMap[track.fileName];
                el.textContent = count !== undefined
                    ? `📥 ${count.toLocaleString()} DL`
                    : '📥 — DL';
            }
        });

    } catch (error) {
        console.error('GitHub API 取得エラー:', error);
        setAllCountsTo('—');
    }
}

function setAllCountsTo(value) {
    TRACKS.forEach(track => {
        const el = document.getElementById(`count-${track.id}`);
        if (el) {
            el.textContent = `📥 ${value} DL`;
        }
    });
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
