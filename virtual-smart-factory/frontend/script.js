const API_URL = "http://127.0.0.1:8000/machines";

// ===============================
// LOAD FACTORY DATA
// ===============================

async function loadFactoryData() {

    try {

        const response = await fetch(API_URL);

        if (!response.ok) {
            throw new Error("API Error: " + response.status);
        }

        const machines = await response.json();

        console.log("Factory data:", machines);

        updateDashboard(machines);

    } catch (error) {

        console.error("Connection error:", error);

        const alerts = document.getElementById("alerts");

        if (alerts) {
            alerts.innerHTML = `
                <div class="alert">
                    <b>🔴 Backend Connection Error</b>
                    <p>${error.message}</p>
                </div>
            `;
        }
    }
}


// ===============================
// DASHBOARD
// ===============================

function updateDashboard(machines) {

    document.getElementById("totalMachines").textContent =
        machines.length;

    const running = machines.filter(machine =>
        machine.status === "Busy" ||
        machine.status === "Running"
    );

    document.getElementById("runningMachines").textContent =
        running.length;


    const down = machines.filter(machine =>
        machine.status === "Maintenance" ||
        machine.status === "Down"
    );

    document.getElementById("downMachines").textContent =
        down.length;


    const bottlenecks = machines.filter(machine =>
        Number(machine.bottleneck) === 1 ||
        Number(machine.queue) >= 15
    );

    document.getElementById("bottlenecks").textContent =
        bottlenecks.length;


    updateMachines(machines);
    updateTable(machines);
    updateAlerts(machines);


    if (machines.length > 0) {
        runAIPrediction(machines[0]);
    }
}


// ===============================
// MACHINE ANIMATION
// ===============================

function updateMachines(machines) {

    machines.forEach(machine => {

        const element =
            document.getElementById(machine.machine_id);

        if (!element) {
            return;
        }


        element.classList.remove(
            "warning",
            "down",
            "idle"
        );


        const temperature =
            Number(machine.temperature);

        const queue =
            Number(machine.queue);


        if (
            machine.status === "Maintenance" ||
            machine.status === "Down"
        ) {

            element.classList.add("down");

        }

        else if (
            temperature >= 70 ||
            queue >= 15
        ) {

            element.classList.add("warning");

        }

        else if (
            machine.status === "Idle"
        ) {

            element.classList.add("idle");

        }


        const info =
            element.querySelector("span");

        if (info) {

            info.textContent =
                `${machine.status} | ${temperature}°C | Queue: ${queue}`;

        }

    });
}


// ===============================
// MACHINE TABLE
// ===============================

function updateTable(machines) {

    const table =
        document.getElementById("machineTable");

    if (!table) {
        return;
    }

    table.innerHTML = "";


    machines.forEach(machine => {

        const row =
            document.createElement("tr");


        row.innerHTML = `

            <td>
                <b>${machine.machine_id}</b>
            </td>

            <td>
                ${machine.status}
            </td>

            <td>
                ${machine.temperature}°C
            </td>

            <td>
                ${machine.queue}
            </td>

            <td>
                ${machine.load}
            </td>

        `;


        table.appendChild(row);

    });
}


// ===============================
// MANAGER ALERTS
// ===============================

function updateAlerts(machines) {

    const alerts =
        document.getElementById("alerts");

    if (!alerts) {
        return;
    }

    alerts.innerHTML = "";

    let alertCount = 0;


    machines.forEach(machine => {

        const temperature =
            Number(machine.temperature);

        const queue =
            Number(machine.queue);


        // MACHINE DOWN

        if (
            machine.status === "Maintenance" ||
            machine.status === "Down"
        ) {

            alerts.innerHTML += `

                <div class="alert">

                    <b>
                    🔴 ${machine.machine_id}
                    - Machine Down
                    </b>

                    <p>
                    Machine status:
                    ${machine.status}
                    </p>

                    <p>
                    Recommendation:
                    Check machine maintenance.
                    </p>

                </div>
            `;

            alertCount++;
        }


        // HIGH TEMPERATURE

        if (temperature >= 70) {

            alerts.innerHTML += `

                <div class="alert warning">

                    <b>
                    🌡️ ${machine.machine_id}
                    - High Temperature
                    </b>

                    <p>
                    Temperature:
                    ${temperature}°C
                    </p>

                    <p>
                    Recommendation:
                    Check cooling system.
                    </p>

                </div>
            `;

            alertCount++;
        }


        // BOTTLENECK

        if (
            Number(machine.bottleneck) === 1 ||
            queue >= 15
        ) {

            alerts.innerHTML += `

                <div class="alert">

                    <b>
                    ⚠️ ${machine.machine_id}
                    - Potential Bottleneck
                    </b>

                    <p>
                    Queue:
                    ${queue}
                    </p>

                    <p>
                    Recommendation:
                    Check machine capacity
                    and production flow.
                    </p>

                </div>
            `;

            alertCount++;
        }

    });


    if (alertCount === 0) {

        alerts.innerHTML = `

            <div class="alert success">

                <b>✅ Factory Normal</b>

                <p>
                No immediate problems detected.
                </p>

            </div>
        `;
    }
}


// ===============================
// AI BOTTLENECK PREDICTION
// ===============================

async function runAIPrediction(machine) {

    const aiBox =
        document.getElementById("aiPrediction");

    if (!aiBox) {
        return;
    }


    try {

        const response = await fetch(
            "http://127.0.0.1:8000/predict-bottleneck",
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({

                    Queue_Length:
                        Number(machine.queue),

                    Processing_Time:
                        Number(machine.processing_time),

                    Temperature:
                        Number(machine.temperature),

                    Previous_Wait_Time: 0,

                    Current_Wait_Time: 0,

                    Machine_Load:
                        Number(machine.load)

                })
            }
        );


        if (!response.ok) {

            throw new Error(
                "AI prediction failed: " +
                response.status
            );

        }


        const result =
            await response.json();


        const machineElement =
            document.getElementById(
                machine.machine_id
            );


        if (result.prediction === 1) {

            if (machineElement) {

                machineElement.classList.add(
                    "warning"
                );

            }


            aiBox.className =
                "ai-bottleneck";


            aiBox.innerHTML = `

                <h3>⚠️ Bottleneck Detected</h3>

                <p>
                    <b>Machine:</b>
                    ${machine.machine_id}
                </p>

                <p>
                    <b>AI Status:</b>
                    ${result.status}
                </p>

                <p>
                    <b>Recommendation:</b>
                    ${result.recommendation}
                </p>

            `;

        }

        else {

            if (machineElement) {

                machineElement.classList.remove(
                    "warning"
                );

            }


            aiBox.className =
                "ai-normal";


            aiBox.innerHTML = `

                <h3>✅ Factory Flow Normal</h3>

                <p>
                    <b>Machine:</b>
                    ${machine.machine_id}
                </p>

                <p>
                    AI detected no immediate bottleneck.
                </p>

            `;
        }


    }

    catch (error) {

        console.error(
            "AI Prediction Error:",
            error
        );


        aiBox.innerHTML = `

            <b>⚠️ AI Prediction unavailable</b>

            <p>
                Check the FastAPI server.
            </p>

        `;
    }
}


// ===============================
// BEARING ANIMATION
// ===============================

function createProduct() {

    const flow =
        document.querySelector(".flow");

    if (!flow) {
        return;
    }


    const product =
        document.createElement("div");

    product.className =
        "moving-product";

    product.innerHTML = "🔩";


    flow.appendChild(product);


    setTimeout(() => {

        product.remove();

    }, 6000);
}


// Create bearing every 4 seconds

setInterval(
    createProduct,
    4000
);


// Load immediately

loadFactoryData();


// Refresh factory data every 3 seconds

setInterval(
    loadFactoryData,
    3000
);