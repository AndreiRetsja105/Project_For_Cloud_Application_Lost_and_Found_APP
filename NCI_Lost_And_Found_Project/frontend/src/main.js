// Import Bootstrap styles, icons and project fonts.
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap-icons/font/bootstrap-icons.css';
import '@fontsource/bricolage-grotesque/600.css';
import '@fontsource/bricolage-grotesque/800.css';
import '@fontsource/atkinson-hyperlegible/400.css';
import '@fontsource/atkinson-hyperlegible/700.css';
import './app.css';

// Import Svelte and the main page component.
import { mount } from 'svelte';
import App from './App.svelte';

// Render the Svelte application inside the HTML element with id="app".
export default mount(App, { target: document.getElementById('app') });