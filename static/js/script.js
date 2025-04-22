let dishCounts = {};

function increaseCount(dishId) {
    if (!dishCounts[dishId]) {
        dishCounts[dishId] = 1;
    } else {
        dishCounts[dishId]++;
    }
    updateDishUI(dishId);
    updateHiddenInput();
}

function decreaseCount(dishId) {
    if (dishCounts[dishId]) {
        dishCounts[dishId]--;
        if (dishCounts[dishId] <= 0) {
            delete dishCounts[dishId];
        }
    }
    updateDishUI(dishId);
    updateHiddenInput();
}

function updateDishUI(dishId) {
    const count = dishCounts[dishId] || 0;
    const countEl = document.getElementById('count-' + dishId);
    const minusEl = document.getElementById('minus-' + dishId);

    if (count > 0) {
        countEl.innerText = count;
        countEl.style.display = 'block';
        minusEl.style.display = 'block';
    } else {
        countEl.style.display = 'none';
        minusEl.style.display = 'none';
    }
}

function updateHiddenInput() {
    const selectedInput = document.getElementById("selectedDishesInput");
    const selectedIds = [];

    for (let id in dishCounts) {
        for (let i = 0; i < dishCounts[id]; i++) {
            selectedIds.push(id);
        }
    }

    selectedInput.value = selectedIds.join(',');
}
