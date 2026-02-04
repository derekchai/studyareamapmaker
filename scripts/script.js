let regions = []

function addRegion() {
    const region = {
        name: document.getElementById("region-name").value || null,
        min_lat: parseFloat(document.getElementById("min-lat").value),
        min_lon: parseFloat(document.getElementById("min-lon").value),
        max_lat: parseFloat(document.getElementById("max-lat").value),
        max_lon: parseFloat(document.getElementById("max-lon").value),
    };

    regions.push(region);

    updateRegionList();
    updateHiddenField();
    clearInputs();
    event.preventDefault();
}

function updateHiddenField() {
    const hidden = document.getElementById("study-regions-hidden-inputs");
    hidden.innerHTML = "";

    regions.forEach((r, i) => {
        const input = document.createElement("input");
        input.name = "study_regions";
        input.value = JSON.stringify(r);
        input.type = "hidden";
        hidden.appendChild(input);
    })

    console.log(hidden.value)
}

function updateRegionList() {
    const list = document.getElementById("region-list");
    list.innerHTML = "";

    regions.forEach((r, i) => {
        const li = document.createElement("li");

        const deleteButton = document.createElement("button");
        deleteButton.textContent = "❌";
        deleteButton.onclick = function () {
            regions.splice(i, 1);
            updateRegionList();
        };

        li.textContent = `${r.name ?? "Unnamed"}: [${r.min_lat}, ${r.min_lon}] → [${r.max_lat}, ${r.max_lon}]`;

        li.appendChild(deleteButton);

        list.appendChild(li);
    })
}

function clearInputs() {
    const inputs = document.getElementById("region-editor").childNodes;

    inputs.forEach((input, i) => {
        input.value = "";
    })
}

document.getElementById("add-region-button").onclick = addRegion;