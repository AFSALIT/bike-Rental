<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Bike Manager - Multi Rental Dashboard</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        :root { --primary: #3498db; --secondary: #2c3e50; --success: #2ecc71; --danger: #e74c3c; }
        body { background: #f8f9fa; }
        .navbar { background: var(--secondary); }
        .card { border-radius: 10px; box-shadow: 0 4px 8px rgba(0,0,0,.08); }
        .status-badge { padding: .25rem .6rem; border-radius: 1rem; font-size: .8rem; }
        .status-Booked { background:#3498db; color:#fff; }
        .status-Active { background:#2980b9; color:#fff; }
        .status-Returned { background:#2ecc71; color:#fff; }
        .status-Cancelled { background:#e74c3c; color:#fff; }
        .table thead th { background:#eef6fd; }
    </style>
</head>
<body>
<nav class="navbar navbar-expand-lg navbar-dark">
    <div class="container">
        <a class="navbar-brand" href="#"><i class="fa fa-bicycle me-2"></i>Bike Manager</a>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#nav"> <span class="navbar-toggler-icon"></span> </button>
        <div class="collapse navbar-collapse" id="nav">
            <ul class="navbar-nav ms-auto">

                <li class="nav-item"><a class="nav-link active" href="/dashboard"><i class="fa fa-layer-group me-1"></i>Multi-Rental Dashboard</a></li>
                <li class="nav-item"><a class="nav-link" href="/purchase-bike"><i class="fa fa-shopping-cart me-1"></i>Purchase Bike</a></li>
                <li class="nav-item"><a class="nav-link" href="/expense"><i class="fa fa-money-bill-wave me-1"></i>Expenses</a></li>
            </ul>
        </div>
    </div>
</nav>

<div class="container mt-4">
    <div class="row g-3">
        <div class="col-lg-4">
            <div class="card">
                <div class="card-body">
                    <div class="d-flex justify-content-between align-items-center mb-3">
                        <h5 class="mb-0">Bikes</h5>
                        <button class="btn btn-primary btn-sm" data-bs-toggle="modal" data-bs-target="#addBikeModal">
                            <i class="fa fa-plus me-1"></i>Add Bike
                        </button>
                    </div>
                    <div class="mb-3">
                        <label class="form-label">Select Bike</label>
                        <select id="bikeSelect" class="form-select">
                            <option value="" selected disabled>Choose a bike...</option>
                        </select>
                    </div>
                    <div id="selectedBikeInfo" class="small text-muted"></div>
                </div>
            </div>
            <div class="card mt-3">
                <div class="card-body">
                    <h6 class="mb-2">Summary</h6>
                    <div class="row text-center">
                        <div class="col-4">
                            <div class="fw-bold" id="summaryTotal">0</div>
                            <div class="text-muted small">Rentals</div>
                        </div>
                        <div class="col-4">
                            <div class="fw-bold" id="summaryActive">0</div>
                            <div class="text-muted small">Active</div>
                        </div>
                        <div class="col-4">
                            <div class="fw-bold" id="summaryRevenue">$0</div>
                            <div class="text-muted small">Revenue</div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div class="col-lg-8">
            <div class="card">
                <div class="card-body">
                    <div class="d-flex justify-content-between align-items-center mb-3">
                        <h5 class="mb-0">Rentals for Selected Bike</h5>
                        <div>
                            <button id="addRentalBtn" class="btn btn-success btn-sm" disabled data-bs-toggle="modal" data-bs-target="#addRentalModal">
                                <i class="fa fa-plus me-1"></i>Add Rental
                            </button>
                        </div>
                    </div>
                    <div class="table-responsive">
                        <table class="table table-sm align-middle" id="rentalsTable">
                            <thead>
                                <tr>
                                    <th>Period</th>
                                    <th>Renter</th>
                                    <th>Contact</th>
                                    <th>Advance</th>
                                    <th>Full Cost</th>
                                    <th>Commission</th>
                                    <th>Status</th>
                                    <th class="text-end">Actions</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr><td colspan="6" class="text-center text-muted">Select a bike to view rentals</td></tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>

<!-- Add Bike Modal -->
<div class="modal fade" id="addBikeModal" tabindex="-1">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <h5 class="modal-title">Add Bike</h5>
        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
      </div>
      <div class="modal-body">
        <form id="addBikeForm">
          <div class="mb-3">
            <label class="form-label">Bike Number *</label>
            <input type="text" class="form-control" id="newBikeNumber" required>
          </div>
          <div class="mb-3">
            <label class="form-label">Bike Name *</label>
            <input type="text" class="form-control" id="newBikeName" required>
          </div>
        </form>
      </div>
      <div class="modal-footer">
        <button class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
        <button class="btn btn-primary" id="submitAddBike">Add Bike</button>
      </div>
    </div>
  </div>
</div>

<!-- Add Rental Modal -->
<div class="modal fade" id="addRentalModal" tabindex="-1">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <h5 class="modal-title">Add Rental</h5>
        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
      </div>
      <div class="modal-body">
        <form id="addRentalForm">
          <div class="row g-2">
            <div class="col-6">
              <label class="form-label">Start Date *</label>
              <input type="date" class="form-control" id="rentStart" required>
            </div>
            <div class="col-6">
              <label class="form-label">End Date *</label>
              <input type="date" class="form-control" id="rentEnd" required>
            </div>
          </div>
          <div class="row g-2 mt-1">
            <div class="col-4">
              <label class="form-label">Advance</label>
              <input type="number" class="form-control" id="rentAdvance" value="0">
            </div>
            <div class="col-4">
              <label class="form-label">Full Cost</label>
              <input type="number" class="form-control" id="rentFullCost" value="0">
            </div>
            <div class="col-4">
              <label class="form-label">Commission</label>
              <input type="number" class="form-control" id="rentCommission" value="0">
            </div>
          </div>
          <div class="mt-2">
            <label class="form-label">Status</label>
            <select class="form-select" id="rentStatus">
              <option>Booked</option>
              <option>Active</option>
              <option>Returned</option>
              <option>Cancelled</option>
            </select>
          </div>
          <!-- New optional renter details -->
          <div class="row g-2 mt-1">
            <div class="col-6">
              <label class="form-label">Renter Name (optional)</label>
              <input type="text" class="form-control" id="rentRenterName" placeholder="John Doe">
            </div>
            <div class="col-6">
              <label class="form-label">Contact No (optional)</label>
              <input type="text" class="form-control" id="rentContactNo" placeholder="+1 555 0100">
            </div>
          </div>
          <div class="mt-2">
            <small>Duration: <span id="addDuration">0 days</span></small>
          </div>
        </form>
      </div>
      <div class="modal-footer">
        <button class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
        <button class="btn btn-success" id="submitAddRental">Add Rental</button>
      </div>
    </div>
  </div>
</div>

<!-- Edit Rental Modal -->
<div class="modal fade" id="editRentalModal" tabindex="-1">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <h5 class="modal-title">Edit Rental</h5>
        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
      </div>
      <div class="modal-body">
        <form id="editRentalForm">
          <input type="hidden" id="editRentalId">
          <div class="row g-2">
            <div class="col-6">
              <label class="form-label">Start Date *</label>
              <input type="date" class="form-control" id="editRentStart" required>
            </div>
            <div class="col-6">
              <label class="form-label">End Date *</label>
              <input type="date" class="form-control" id="editRentEnd" required>
            </div>
          </div>
          <div class="row g-2 mt-1">
            <div class="col-4">
              <label class="form-label">Advance</label>
              <input type="number" class="form-control" id="editRentAdvance" value="0">
            </div>
            <div class="col-4">
              <label class="form-label">Full Cost</label>
              <input type="number" class="form-control" id="editRentFullCost" value="0">
            </div>
            <div class="col-4">
              <label class="form-label">Commission</label>
              <input type="number" class="form-control" id="editRentCommission" value="0">
            </div>
          </div>
          <div class="mt-2">
            <label class="form-label">Status</label>
            <select class="form-select" id="editRentStatus">
              <option>Booked</option>
              <option>Active</option>
              <option>Returned</option>
              <option>Cancelled</option>
            </select>
          </div>
          <!-- New optional renter details for edit -->
          <div class="row g-2 mt-1">
            <div class="col-6">
              <label class="form-label">Renter Name (optional)</label>
              <input type="text" class="form-control" id="editRenterName" placeholder="John Doe">
            </div>
            <div class="col-6">
              <label class="form-label">Contact No (optional)</label>
              <input type="text" class="form-control" id="editContactNo" placeholder="+1 555 0100">
            </div>
          </div>
          <div class="mt-2">
            <small>Duration: <span id="editDuration">0 days</span></small>
          </div>
        </form>
      </div>
      <div class="modal-footer">
        <button class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
        <button class="btn btn-primary" id="submitEditRental">Save Changes</button>
      </div>
    </div>
  </div>
</div>

<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
<script>
  const API_BASE = '';
  const bikeSelect = document.getElementById('bikeSelect');
  const selectedBikeInfo = document.getElementById('selectedBikeInfo');
  const addRentalBtn = document.getElementById('addRentalBtn');
  const rentalsTableBody = document.querySelector('#rentalsTable tbody');
  const summaryTotal = document.getElementById('summaryTotal');
  const summaryActive = document.getElementById('summaryActive');
  const summaryRevenue = document.getElementById('summaryRevenue');

  let currentBike = null;

  document.addEventListener('DOMContentLoaded', () => {
    loadBikes();
    document.getElementById('submitAddBike').addEventListener('click', onAddBike);
    document.getElementById('submitAddRental').addEventListener('click', onAddRental);
    document.getElementById('submitEditRental').addEventListener('click', onEditRental);
    bikeSelect.addEventListener('change', onBikeChange);

    // Add event listeners to update duration on date change in Add Rental modal
    document.getElementById('rentStart').addEventListener('change', updateAddDuration);
    document.getElementById('rentEnd').addEventListener('change', updateAddDuration);

    // Add event listeners to update duration on date change in Edit Rental modal
    document.getElementById('editRentStart').addEventListener('change', updateEditDuration);
    document.getElementById('editRentEnd').addEventListener('change', updateEditDuration);
  });

  function updateAddDuration() {
    const start = document.getElementById('rentStart').value;
    const end = document.getElementById('rentEnd').value;
    const durationSpan = document.getElementById('addDuration');
    const days = calculateDays(start, end);
    durationSpan.textContent = `${days} days`;
  }

  function updateEditDuration() {
    const start = document.getElementById('editRentStart').value;
    const end = document.getElementById('editRentEnd').value;
    const durationSpan = document.getElementById('editDuration');
    const days = calculateDays(start, end);
    durationSpan.textContent = `${days} days`;
  }

  async function loadBikes() {
    try {
      const res = await fetch(`${API_BASE}/bikes`);
      const data = await res.json();
      renderBikeOptions(data.bikes || []);
    } catch (e) { alert('Failed to load bikes'); }
  }

  function renderBikeOptions(bikes) {
    bikeSelect.innerHTML = '<option value="" disabled selected>Choose a bike...</option>';
    bikes.forEach(b => {
      const opt = document.createElement('option');
      opt.value = b.bike_number;
      opt.textContent = `${b.bike_number} - ${b.bike_name}`;
      opt.dataset.name = b.bike_name || '';
      bikeSelect.appendChild(opt);
    });
  }

  async function onBikeChange() {
    const number = bikeSelect.value;
    const name = bikeSelect.options[bikeSelect.selectedIndex].dataset.name || '';
    currentBike = { bike_number: number, bike_name: name };
    selectedBikeInfo.textContent = `Selected: ${number} ${name ? '(' + name + ')' : ''}`;
    addRentalBtn.disabled = false;
    await loadRentals(number);
  }

  async function loadRentals(bikeNumber) {
    rentalsTableBody.innerHTML = '<tr><td colspan="5" class="text-muted text-center">Loading...</td></tr>';
    try {
      const res = await fetch(`${API_BASE}/bikes/${bikeNumber}/rentals`);
      if (!res.ok) throw new Error('Load rentals failed');
      const data = await res.json();
      renderRentals(data.rentals || []);
    } catch (e) {
      rentalsTableBody.innerHTML = '<tr><td colspan="5" class="text-danger text-center">Failed to load rentals</td></tr>';
    }
  }

  function renderRentals(rentals) {
    if (!rentals.length) {
      rentalsTableBody.innerHTML = '<tr><td colspan="5" class="text-muted text-center">No rentals yet</td></tr>';
      updateSummary([]);
      return;
    }
    rentalsTableBody.innerHTML = '';
    rentals.forEach(r => {
      const days = calculateDays(r.rent_start_date, r.rent_end_date);
      const tr = document.createElement('tr');
      tr.innerHTML = `
        <td>${formatDate(r.rent_start_date)} - ${formatDate(r.rent_end_date)} (${days} days)</td>
        <td>${(r.renter_name || '').toString()}</td>
        <td>${(r.contact_no || '').toString()}</td>
        <td>$${fmtNum(r.advance)}</td>
        <td>$${fmtNum(r.full_cost)}</td>
        <td>$${fmtNum(r.commission || 0)}</td>
        <td>
          <select class="form-select form-select-sm status-select" data-id="${r.rental_id}">
            <option value="Booked" ${r.status === 'Booked' ? 'selected' : ''}>Booked</option>
            <option value="Active" ${r.status === 'Active' ? 'selected' : ''}>Active</option>
            <option value="Returned" ${r.status === 'Returned' ? 'selected' : ''}>Returned</option>
            <option value="Cancelled" ${r.status === 'Cancelled' ? 'selected' : ''}>Cancelled</option>
          </select>
        </td>
        <td class="text-end">
          <button class="btn btn-sm btn-outline-primary me-1" data-action="edit" data-id="${r.rental_id}"><i class="fa fa-edit"></i></button>
          <button class="btn btn-sm btn-outline-danger" data-action="delete" data-id="${r.rental_id}"><i class="fa fa-trash"></i></button>
        </td>`;
      rentalsTableBody.appendChild(tr);
    });
    rentalsTableBody.querySelectorAll('button').forEach(btn => btn.addEventListener('click', onRentalAction));
    rentalsTableBody.querySelectorAll('.status-select').forEach(sel => sel.addEventListener('change', onStatusChange));
    updateSummary(rentals);
  }

  function updateSummary(rentals) {
    summaryTotal.textContent = rentals.length;
    summaryActive.textContent = rentals.filter(r => r.status === 'Active').length;
    const revenue = rentals.reduce((s, r) => s + (parseFloat(r.full_cost) || 0), 0);
    summaryRevenue.textContent = `$${revenue.toFixed(2)}`;
    const commission = rentals.reduce((s, r) => s + (parseFloat(r.commission) || 0), 0);
    // Optionally add to summary, but since summary has only 3 cols, maybe add to revenue or create new
    // For now, append to revenue text
    summaryRevenue.textContent = `$${revenue.toFixed(2)} (Comm: $${commission.toFixed(2)})`;
  }

  async function onAddBike() {
    const bike_number = document.getElementById('newBikeNumber').value.trim();
    const bike_name = document.getElementById('newBikeName').value.trim();
    if (!bike_number || !bike_name) { alert('Both fields are required'); return; }
    try {
      const res = await fetch(`${API_BASE}/bikes`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ bike_number, bike_name }) });
      if (!res.ok) { const e = await res.json(); throw new Error(e.error || 'Add bike failed'); }
      document.getElementById('addBikeForm').reset();
      bootstrap.Modal.getInstance(document.getElementById('addBikeModal')).hide();
      await loadBikes();
      // Auto-select the newly added bike
      bikeSelect.value = bike_number; bikeSelect.dispatchEvent(new Event('change'));
    } catch (e) { alert(e.message); }
  }

  async function onAddRental() {
    if (!currentBike) return;
    const payload = {
      rent_start_date: document.getElementById('rentStart').value,
      rent_end_date: document.getElementById('rentEnd').value,
      advance: document.getElementById('rentAdvance').value || 0,
      full_cost: document.getElementById('rentFullCost').value || 0,
      commission: document.getElementById('rentCommission').value || 0,
      status: document.getElementById('rentStatus').value,
      bike_name: currentBike.bike_name || '',
      renter_name: document.getElementById('rentRenterName').value || '',
      contact_no: document.getElementById('rentContactNo').value || ''
    };
    if (!payload.rent_start_date || !payload.rent_end_date) { alert('Dates are required'); return; }
    try {
      const res = await fetch(`${API_BASE}/bikes/${currentBike.bike_number}/rentals`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload) });
      if (!res.ok) { const e = await res.json(); throw new Error(e.error || 'Add rental failed'); }
      document.getElementById('addRentalForm').reset();
      bootstrap.Modal.getInstance(document.getElementById('addRentalModal')).hide();
      await loadRentals(currentBike.bike_number);
    } catch (e) { alert(e.message); }
  }

  function onRentalAction(ev) {
    const btn = ev.currentTarget;
    const action = btn.dataset.action;
    const rentalId = btn.dataset.id;
    if (action === 'delete') return deleteRental(rentalId);
    if (action === 'edit') return openEditRental(rentalId);
  }

  async function openEditRental(rentalId) {
    try {
      const res = await fetch(`${API_BASE}/bikes/${currentBike.bike_number}/rentals/${rentalId}`);
      if (!res.ok) throw new Error('Load rental failed');
      const r = await res.json();
      document.getElementById('editRentalId').value = r.rental_id;
      document.getElementById('editRentStart').value = r.rent_start_date || '';
      document.getElementById('editRentEnd').value = r.rent_end_date || '';
      document.getElementById('editRentAdvance').value = r.advance || 0;
      document.getElementById('editRentFullCost').value = r.full_cost || 0;
      document.getElementById('editRentCommission').value = r.commission || 0;
      document.getElementById('editRentStatus').value = r.status || 'Booked';
      document.getElementById('editRenterName').value = r.renter_name || '';
      document.getElementById('editContactNo').value = r.contact_no || '';
      updateEditDuration(); // Update duration display
      new bootstrap.Modal(document.getElementById('editRentalModal')).show();
    } catch (e) { alert(e.message); }
  }

  async function onEditRental() {
    const rentalId = document.getElementById('editRentalId').value;
    const payload = {
      rent_start_date: document.getElementById('editRentStart').value,
      rent_end_date: document.getElementById('editRentEnd').value,
      advance: document.getElementById('editRentAdvance').value || 0,
      full_cost: document.getElementById('editRentFullCost').value || 0,
      commission: document.getElementById('editRentCommission').value || 0,
      status: document.getElementById('editRentStatus').value,
      renter_name: document.getElementById('editRenterName').value || '',
      contact_no: document.getElementById('editContactNo').value || ''
    };
    if (!payload.rent_start_date || !payload.rent_end_date) { alert('Dates are required'); return; }
    try {
      const res = await fetch(`${API_BASE}/bikes/${currentBike.bike_number}/rentals/${rentalId}`, { method: 'PUT', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload) });
      if (!res.ok) throw new Error('Update rental failed');
      bootstrap.Modal.getInstance(document.getElementById('editRentalModal')).hide();
      await loadRentals(currentBike.bike_number);
    } catch (e) { alert(e.message); }
  }

  async function deleteRental(rentalId) {
    if (!confirm('Delete this rental?')) return;
    try {
      const res = await fetch(`${API_BASE}/bikes/${currentBike.bike_number}/rentals/${rentalId}`, { method: 'DELETE' });
      if (!res.ok) throw new Error('Delete failed');
      await loadRentals(currentBike.bike_number);
    } catch (e) { alert(e.message); }
  }

  function formatDate(s) { if (!s) return 'N/A'; return new Date(s).toLocaleDateString(); }
  function fmtNum(n) { const v = parseFloat(n)||0; return v.toFixed(2); }
  function calculateDays(startDate, endDate) {
    if (!startDate || !endDate) return 0;
    const start = new Date(startDate);
    const end = new Date(endDate);
    const diffTime = Math.abs(end - start);
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
    return diffDays;
  }

  async function onStatusChange(event) {
    const select = event.target;
    const rentalId = select.dataset.id;
    const newStatus = select.value;
    if (!currentBike || !rentalId) return;
    try {
      const res = await fetch(`${API_BASE}/bikes/${currentBike.bike_number}/rentals/${rentalId}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ status: newStatus })
      });
      if (!res.ok) throw new Error('Failed to update status');
      // Optionally, update summary or show a success message
      await loadRentals(currentBike.bike_number);
    } catch (e) {
      alert(e.message);
      // Revert select to previous value on error
      await loadRentals(currentBike.bike_number);
    }
  }
</script>
</body>
</html>
