document.addEventListener("DOMContentLoaded", function () {
  const form = document.getElementById("kiForm");
  form.addEventListener("submit", async function (e) {
    e.preventDefault();

    const formData = new FormData(form);
    const data = Object.fromEntries(formData.entries());

    // Partnerkennung aus der URL extrahieren
    const params = new URLSearchParams(window.location.search);
    const partner = params.get("partner") || "default";

    try {
      const response = await fetch(`https://make.ki-sicherheit.jetzt/analyze?partner=${partner}`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ answers: data })
      });

      if (!response.ok) {
        throw new Error("Serverfehler: " + response.status);
      }

      const result = await response.json();

      // Beispiel: Nur Summary anzeigen – später: PDF oder Link
      alert("Analyse abgeschlossen!\n\nZusammenfassung:\n" + result.report);

      // Optional: Weiterleitung zu danke.html
      window.location.href = "/formular/danke.html";

    } catch (error) {
      console.error("Fehler bei der Analyse:", error);
      alert("Leider ist ein Fehler aufgetreten. Bitte versuchen Sie es später erneut.");
    }
  });
});