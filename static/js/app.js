(function () {
    /* === Dark mode toggle === */
    var html = document.documentElement;
    var saved = localStorage.getItem('theme');
    if (saved === 'dark') html.classList.add('dark');
    if (!saved && window.matchMedia('(prefers-color-scheme: dark)').matches) html.classList.add('dark');

    function toggleTheme() {
        html.classList.toggle('dark');
        localStorage.setItem('theme', html.classList.contains('dark') ? 'dark' : 'light');
    }

    document.addEventListener('DOMContentLoaded', function () {
        var btn = document.getElementById('theme-toggle');
        if (btn) btn.addEventListener('click', toggleTheme);
    });

    /* === Anonymous identity === */
    var NICKNAMES = [
        'Echoes', 'Time', 'Money', 'Shine On', 'Comfortably Numb',
        'Wish You Were Here', 'Brain Damage', 'Breathe', 'Us and Them',
        'Hey You', 'Dogs', 'Sheep', 'Pigs', 'One Slip',
        'Marooned', 'Astronomy Domine', 'Lucifer Sam', 'See-Saw',
        'Julia Dream', 'Remember a Day'
    ];

    var AVATAR_TYPES = ['circle', 'square', 'triangle', 'cross'];
    var AVATAR_COLORS = ['#e63946', '#2563eb', '#f4d03f', '#1a1a2e', '#10b981'];

    function rand(arr) { return arr[Math.floor(Math.random() * arr.length)]; }

    function getIdentity() {
        try {
            var stored = localStorage.getItem('anon-identity');
            if (stored) return JSON.parse(stored);
        } catch (_) {}
        var identity = {
            name: rand(NICKNAMES),
            avatar: rand(AVATAR_TYPES),
            color: rand(AVATAR_COLORS)
        };
        localStorage.setItem('anon-identity', JSON.stringify(identity));
        return identity;
    }

    /* Wire up comment forms: inject hidden author field */
    document.addEventListener('DOMContentLoaded', function () {
        var identity = getIdentity();
        var forms = document.querySelectorAll('.comment-form');
        for (var i = 0; i < forms.length; i++) {
            var hidden = document.createElement('input');
            hidden.type = 'hidden';
            hidden.name = 'author';
            hidden.value = identity.name;
            forms[i].appendChild(hidden);
        }
    });

    /* Expose for template use */
    window.getAnonIdentity = getIdentity;
})();
