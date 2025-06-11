// Affichage d'une évaluation fictive des compétences (à enrichir avec données réelles).
import React from "react";

const SkillsEvaluation = () => (
  <section className="mb-8">
    <h3 className="text-xl font-semibold mb-2 text-blue-700">Évaluation des compétences</h3>
    <div className="bg-blue-100 p-4 rounded">
      {/* Ici, on pourrait afficher les compétences sous forme de progress bars ou graphiques */}
      <p>
        Exemple: Python <span className="inline-block w-40 bg-blue-700 h-2 rounded mx-2 align-middle"></span> 90%
      </p>
      <p>
        SQL <span className="inline-block w-32 bg-blue-700 h-2 rounded mx-2 align-middle"></span> 70%
      </p>
      {/* À remplacer par les vraies données issues de l'analyse NLP */}
    </div>
  </section>
);

export default SkillsEvaluation;