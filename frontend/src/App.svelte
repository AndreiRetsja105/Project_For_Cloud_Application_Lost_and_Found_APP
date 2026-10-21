<script>
  import { onMount } from 'svelte';
  import { getItems, createItem, updateItem, deleteItem } from './lib/api.js';

  const blankItem = () => ({ title: '', description: '', category: 'lost', location: '', status: 'open' });
  let items = $state([]);
  let filter = $state('');
  let form = $state(blankItem());
  let editingId = $state(null);
  let loading = $state(false);
  let saving = $state(false);
  let error = $state('');
  let notice = $state('');

  /** Refresh the reports each time the filter changes or a record is updated. */
  async function loadItems() {
    loading = true;
    error = '';
    try { items = await getItems(filter); }
    catch (err) { error = `Could not load reports: ${err.message}`; }
    finally { loading = false; }
  }

  /** Create a record or replace the selected one through the REST API. */
  async function saveItem(event) {
    event.preventDefault();
    saving = true;
    error = '';
    notice = '';
    try {
      if (editingId === null) {
        await createItem(form);
        notice = 'Report created successfully.';
      } else {
        await updateItem(editingId, form);
        notice = 'Report updated successfully.';
      }
      cancelEdit();
      await loadItems();
    } catch (err) { error = `Could not save report: ${err.message}`; }
    finally { saving = false; }
  }

  /** Copy the selected report into the form for editing. */
  function startEdit(item) {
    editingId = item.id;
    form = { title: item.title, description: item.description, category: item.category, location: item.location, status: item.status };
    notice = '';
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }

  /** Return the form to create mode without changing the database. */
  function cancelEdit() {
    editingId = null;
    form = blankItem();
  }

  /** Ask for confirmation before deleting a report permanently. */
  async function removeItem(item) {
    if (!window.confirm(`Delete report #${item.id}: ${item.title}?`)) return;
    error = '';
    notice = '';
    try {
      await deleteItem(item.id);
      if (editingId === item.id) cancelEdit();
      notice = `Report #${item.id} deleted.`;
      await loadItems();
    } catch (err) { error = `Could not delete report: ${err.message}`; }
  }

  onMount(loadItems);
</script>

<svelte:head>
  <title>NCI Lost & Found | Reports</title>
  <meta name="description" content="Report and browse lost and found items at NCI" />
</svelte:head>


<header class="nci-hero">
  <div class="nci-hero-overlay"></div>

  <div class="container nci-hero-content">
    <div class="d-flex justify-content-between align-items-center mb-4">
      <!-- Display the NCI logo at the top of the page. -->
      <img
        src="/nci-logo.png"
        alt="National College of Ireland"
        class="nci-logo"
      />

      <span class="badge rounded-pill text-bg-light px-3 py-2">
        Svelte + FastAPI + SQLite
      </span>
    </div>

    <p class="site-kicker text-uppercase">
      Cloud Application Development · v0.4
    </p>

    <h1>NCI Lost & Found</h1>

    <p class="hero-subtitle">
      Report and manage lost or found items on campus
    </p>
  </div>
</header>

<main class="container pb-5">
  {#if error}<div class="alert alert-danger" role="alert">{error}</div>{/if}
  {#if notice}<div class="alert alert-success" role="status">{notice}</div>{/if}
  <div class="row g-4">
    <section class="col-lg-5" aria-label="Report an item">
      <div class="card shadow-sm border-0 sticky-form">
        <div class="card-body p-4">
          <h2 class="h4 mb-2">{editingId === null ? 'Report an item' : `Edit report #${editingId}`}</h2>
          <p class="text-secondary small">Fields are validated by FastAPI before saving.</p>
          <form onsubmit={saveItem}>
            <div class="mb-3"><label class="form-label" for="title">Item title</label><input id="title" class="form-control" required minlength="3" maxlength="100" bind:value={form.title} placeholder="e.g. Black backpack" /></div>
            <div class="mb-3"><label class="form-label" for="description">Description</label><textarea id="description" class="form-control" rows="3" required minlength="5" maxlength="500" bind:value={form.description} placeholder="How does the item look?"></textarea></div>
            <div class="row g-3 mb-3"><div class="col-6"><label class="form-label" for="category">Category</label><select id="category" class="form-select" bind:value={form.category}><option value="lost">Lost</option><option value="found">Found</option></select></div><div class="col-6"><label class="form-label" for="status">Status</label><select id="status" class="form-select" bind:value={form.status}><option value="open">Open</option><option value="lost">Lost</option><option value="found">Found</option><option value="resolved">Resolved</option></select></div></div>
            <div class="mb-3"><label class="form-label" for="location">Location</label><input id="location" class="form-control" required minlength="2" maxlength="120" bind:value={form.location} placeholder="e.g. NCI library" /></div>
            <div class="d-flex gap-2"><button class="btn btn-primary" type="submit" disabled={saving}>{saving ? 'Saving…' : editingId === null ? 'Add report' : 'Save changes'}</button>{#if editingId !== null}<button class="btn btn-outline-secondary" type="button" onclick={cancelEdit}>Cancel</button>{/if}</div>
          </form>
        </div>
      </div>
    </section>
    <section class="col-lg-7" aria-label="Browse reports">
      <div class="d-flex flex-wrap align-items-center justify-content-between gap-2 mb-3"><div><h2 class="h4 mb-1">Campus reports</h2><p class="text-secondary small mb-0">Browse items saved in SQLite</p></div><div class="d-flex gap-2"><select class="form-select" aria-label="Filter reports by category" bind:value={filter} onchange={loadItems}><option value="">All items</option><option value="lost">Lost</option><option value="found">Found</option></select><button class="btn btn-outline-primary" type="button" onclick={loadItems}>Refresh</button></div></div>
      {#if loading}<p class="text-secondary" role="status">Loading reports…</p>
      {:else if items.length === 0}<div class="empty-state p-4 text-center"><h3 class="h5">No reports yet</h3><p class="text-secondary mb-0">Add the first report using the form.</p></div>
      {:else}<div class="d-grid gap-3">{#each items as item (item.id)}<article class="card report-card border-0 shadow-sm"><div class="card-body p-3"><div class="d-flex justify-content-between align-items-start gap-2"><div><div class="d-flex gap-2 mb-2"><span class:lost={item.category === 'lost'} class:found={item.category === 'found'} class="category-pill">{item.category}</span><span class="badge text-bg-light">{item.status}</span></div><h3 class="h5 mb-1">{item.title}</h3></div><small class="text-secondary">#{item.id}</small></div><p class="mt-2 mb-2">{item.description}</p><p class="text-secondary small mb-3"><i class="bi bi-geo-alt"></i> {item.location}</p><div class="d-flex gap-2"><button class="btn btn-sm btn-outline-primary" type="button" onclick={() => startEdit(item)}>Edit</button><button class="btn btn-sm btn-outline-danger" type="button" onclick={() => removeItem(item)}>Delete</button></div></div></article>{/each}</div>{/if}
    </section>
  </div>
</main>
