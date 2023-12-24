function showDetails(orderId, carrierTrackingNumber, orderQty, unitPrice, totalPrice, productName, productNumber, color, storeName) {
    document.getElementById('tab1').innerHTML = `
        <p><strong>Order ID:</strong> ${orderId}</p>
        <p>Carrier Tracking Number: ${carrierTrackingNumber}</p>
        <p>Order Quantity: ${orderQty}</p>
        <p>Unit Price: ${unitPrice}</p>
        <p>Total Price: ${totalPrice}</p>
    `;

    document.getElementById('tab2').innerHTML = `
        <p><strong>Order ID:</strong> ${orderId}</p>
        <p>Product Name: ${productName}</p>
        <p>Product Number: ${productNumber}</p>
        <p>Store Name: ${storeName}</p>
    `;

    document.getElementById('detailPopup').style.display = 'block';
}

function closePopup() {
    document.getElementById('detailPopup').style.display = 'none';
}

function openTab(event, tabName) {
    let i, tabContent, tabs;
    tabContent = document.getElementsByClassName("tab-content");
    for (i = 0; i < tabContent.length; i++) {
        tabContent[i].style.display = "none";
    }
    tabs = document.getElementsByClassName("tabs")[0].getElementsByTagName("li");
    for (i = 0; i < tabs.length; i++) {
        tabs[i].className = tabs[i].className.replace(" active", "");
    }
    document.getElementById(tabName).style.display = "block";
    event.currentTarget.className += " active";
}

function toggleColumns() {
    const showColumnsCheckbox = document.getElementById('showColumns');
    const columns = document.querySelectorAll('.toggle-column');

    for (let i = 0; i < columns.length; i++) {
        columns[i].style.display = showColumnsCheckbox.checked ? 'table-cell' : 'none';
    }
}

document.addEventListener("DOMContentLoaded", function () {
    const statusCells = document.querySelectorAll(".status-cell");

    statusCells.forEach(cell => {
        cell.addEventListener("mouseover", showLegend);
        cell.addEventListener("mouseout", hideLegend);
    });

    function showLegend(event) {
        const status = event.target.dataset.status;
        const legendTooltip = document.getElementById("legendTooltip");

        legendTooltip.innerHTML = getStatusLegend(status);
        legendTooltip.style.left = event.pageX + "px";
        legendTooltip.style.top = event.pageY + "px";
        legendTooltip.style.display = "block";
    }

    function hideLegend() {
        const legendTooltip = document.getElementById("legendTooltip");
        legendTooltip.style.display = "none";
    }

    function getStatusLegend(statusCode) {
        switch (parseInt(statusCode)) {
            case 1:
                return "In Process";
            case 2:
                return "Approved";
            case 3:
                return "Back Ordered";
            case 4:
                return "Rejected";
            case 5:
                return "Shipped";
            case 6:
                return "Cancelled";
            default:
                return "Unknown Status";
        }
    }
})


