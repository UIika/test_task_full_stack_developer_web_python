function showTooltip(event) {
    const tooltip = event.currentTarget.querySelector('.tooltip');
    tooltip.style.display = 'block';
}

function hideTooltip(event) {
    const tooltip = event.currentTarget.querySelector('.tooltip');
    tooltip.style.display = 'none';
}