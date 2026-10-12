<script>
  // The project name is used in the page title and heading.
  const projectName = 'NCI Lost and Found';
</script>

<!-- the browser tab title and page description. -->
<svelte:head>
  <title>{projectName}</title>
  <meta name="description" content="Student lost and found SaaS project" />
</svelte:head>

<!-- Main content of the page. -->
<main class="container py-5">
  <div class="mx-auto" style="max-width: 760px">
    <p class="text-primary fw-bold">Cloud Application Development · Version 0.1</p>
    <h1 class="display-4 fw-bold">{projectName}</h1>
    <p class="lead">A cloud based lost and found service for the National College of Ireland.</p>
    <!-- What is available in this version. -->
    <div class="alert alert-info mt-4" role="status">
      Initial project setup. Reporting items, search and matching will be added in future versions.
    </div>
    <!-- Features to implement the next development stages. -->
    <h2 class="h5 mt-5">Planned features</h2>
    <ul>
      <li>Report lost and found items</li>
      <li>Browse and manage reports</li>
      <li>Suggest possible matches</li>
    </ul>
  </div>
</main>