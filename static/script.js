async function loadOrders() {
    try {
        const response = await fetch('http://127.0.0.1:8000/orders');
        const orders = await response.json();
        
        const tableBody = document.getElementById('po-table-body');
        tableBody.innerHTML = ''; // Clear existing rows

        orders.forEach(order => {
           // This part goes inside your loadOrders function
const row = `
    <tr>
        <td>${order.reference_no}</td>
        <td>${order.vendor_id}</td>
        <td class="text-end">₹${parseFloat(order.total_amount).toFixed(2)}</td> 
        <td><span class="badge bg-success">${order.status}</span></td>
    </tr>
`;
            tableBody.innerHTML += row;
        });
    } catch (error) {
        console.error("Error loading orders:", error);
    }
}

// Load data when the page opens
window.onload = loadOrders;