// Affichage d'un aperçu du CV (statique ou dynamique selon besoin).
// Peut être enrichi pour affichage stylisé ou PDF.
import React from "react";

const CVPreview = () => (
  <section className="mb-8">
    <h3 className="text-xl font-semibold mb-2 text-blue-700">Aperçu du CV</h3>
    <div className="bg-gray-50 p-4 rounded shadow">
      <p>
        Ici, un aperçu du CV sera généré à partir des données saisies ou analysées.
      </p>
      {/* À compléter avec un rendu réel du CV */}
    </div>
  </section>
);

export default CVPreview;