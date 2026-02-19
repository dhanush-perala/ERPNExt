(function () {
	if (window.__urscSplineLoaderInitialized) return;
	window.__urscSplineLoaderInitialized = true;

	function shouldShow() {
		try {
			var path = (window.location && window.location.pathname) || '';
			if (path.indexOf('/login') !== -1) return true;
			if (document.querySelector('form#login_form')) return true;
			return false;
		} catch (e) {
			return false;
		}
	}

	function createLoader() {
		var overlay = document.createElement('div');
		overlay.id = 'ursc-spline-loader-overlay';
		overlay.style.position = 'fixed';
		overlay.style.inset = '0';
		overlay.style.background = '#0b0f1a';
		overlay.style.zIndex = '99999';
		overlay.style.display = 'flex';
		overlay.style.alignItems = 'center';
		overlay.style.justifyContent = 'center';
		overlay.style.transition = 'opacity 200ms ease';

		var container = document.createElement('div');
		container.style.width = 'min(720px, 90vw)';
		container.style.height = 'min(420px, 60vh)';
		container.style.maxWidth = '100%';
		container.style.maxHeight = '100%';

		var script = document.createElement('script');
		script.type = 'module';
		script.src = 'https://unpkg.com/@splinetool/viewer@1.10.61/build/spline-viewer.js';

		var viewer = document.createElement('spline-viewer');
		viewer.setAttribute('url', 'https://prod.spline.design/dLBI2O8BLFrn38d2/scene.splinecode');
		viewer.style.width = '100%';
		viewer.style.height = '100%';
		viewer.style.border = '0';

		container.appendChild(viewer);
		overlay.appendChild(container);

		document.head.appendChild(script);
		document.body.appendChild(overlay);

		return overlay;
	}

	function removeLoader(overlay) {
		if (!overlay) return;
		overlay.style.opacity = '0';
		setTimeout(function () {
			if (overlay && overlay.parentNode) {
				overlay.parentNode.removeChild(overlay);
			}
		}, 220);
	}

	function init() {
		if (!shouldShow()) return;

		// If a generic overlay container exists on login, hide it to avoid covering the card
		try {
			var conflicting = document.getElementById('container');
			if (conflicting) {
				conflicting.style.display = 'none';
			}
		} catch (e) {}
		var overlay = createLoader();

		var done = false;
		function finish() {
			if (done) return; done = true;
			removeLoader(overlay);
		}

		// Fallbacks: DOM ready + load + max timeout (login page is mostly static)
		document.addEventListener('DOMContentLoaded', function () {
			setTimeout(finish, 800);
		});
		window.addEventListener('load', function () {
			setTimeout(finish, 600);
		});
		setTimeout(finish, 4000);
	}

	if (document.readyState === 'loading') {
		document.addEventListener('DOMContentLoaded', init);
	} else {
		init();
	}
})();


