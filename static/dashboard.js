async function sendCommand() {
  let command = document.getElementById("command").value;

  let response = await fetch("/terminal", {
    method: "POST",

    headers: {
      "Content-Type": "application/json",
    },

    body: JSON.stringify({
      command: command,
    }),
  });

  let data = await response.json();

  document.getElementById("terminal").textContent = data.output + data.error;
}

async function restartPi() {
  let response = await fetch("/reboot", {
    method: "POST",
  });

  let data = await response.json();

  document.getElementById("status").textContent = data.status;
}

async function refresh() {
  let res = await fetch("/refresh", { method: "POST" });
  let data = await res.json();

  document.getElementById("refresh-status").innerText = data.status;
}
