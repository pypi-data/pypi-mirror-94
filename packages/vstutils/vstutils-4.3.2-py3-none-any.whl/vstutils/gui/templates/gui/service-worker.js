//{% load request_static %}
//{% load cache %}
//{% cache block_timeout service_worker_block gui_version %}
//{% autoescape off %}
importScripts("{% static 'bundle/workbox/workbox-sw.js' %}");

const GUI_VERSION = '{{ gui_version }}';

workbox.setConfig({
  modulePathPrefix: "{% static 'bundle/workbox/' %}",
  debug: false,
});

workbox.core.skipWaiting();
workbox.core.clientsClaim();
/**
 * Array of static files paths.
 * These files will be added to the page by JS.
 * They are not included in the page template as html tags.
 */
const STATIC_FILES_LIST = [
//{% for static_file in static_files_list %}
    '{% static static_file.name %}',
//{% endfor %}
];

/**
 * Path of Offline fallback page.
 */
//{% block offline_page %}
const OFFLINE_PAGE = '/offline.html';
//{% endblock %}

/**
 * Path to the favicon file.
 */
//{% block favicon %}
const FAVICON = "{% static 'img/logo/favicon.ico' %}";
//{% endblock %}

/**
 * Path to the app loader file.
 */
//{% block app_loader %}
const APP_LOADER = "{% static 'bundle/app_loader.js' %}";
//{% endblock %}

/**
 * Path to PWA icons.
 */
const PWA_ICONS_LIST = [
// {% for icon in manifest_object.icons %}
    "{{ icon.src }}",
//{% endfor %}
];

/**
 * Array with paths of additional files, that should precached.
 */
//{% block resource_list %}
const ADDITIONAL_FILES_LIST = [];
//{% endblock %}

/**
 * Array, that store paths of files, that should be precached.
 */
const PRECACHE_LIST = [OFFLINE_PAGE, FAVICON, APP_LOADER].concat(STATIC_FILES_LIST, ADDITIONAL_FILES_LIST, PWA_ICONS_LIST)
    .map(filePath => ({ url: filePath, revision: GUI_VERSION }));

/**
 * Sets workbox cache names details.
 * From these elements will be formed precache and runtime caches.
 */
workbox.core.setCacheNameDetails({
    prefix: '{{ project_gui_name }}',
    suffix: 'v{{gui_version}}',
    precache: 'static',
    runtime: 'run-time',
});

/**
 * Adds precaching of PRECACHE_LIST.
 */
workbox.precaching.precacheAndRoute(PRECACHE_LIST);

/**
 * Deletes cache of previous (outdated) versions.
 */
self.addEventListener('activate', event => {
    let cacheWhitelist = [workbox.core.cacheNames.precache, workbox.core.cacheNames.runtime];
    event.waitUntil(
        caches.keys().then(keyList => {
            return Promise.all(keyList.map(key => {
                if (cacheWhitelist.indexOf(key) === -1) {
                    return caches.delete(key);
                }
            }));
        })
    );
});

/**
 * Handling offline requests to html docs.
 */
self.addEventListener('fetch', (event) => {
    let request = event.request;

    if (request.method === 'GET' && request.headers.get('accept').includes('text/html')) {
        event.respondWith(
            fetch(request).catch((error) => caches.match(OFFLINE_PAGE))
        );
    }
});
//{% endautoescape %}
//{% endcache %}