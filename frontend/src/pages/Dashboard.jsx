// Dashboard principal : permet de créer un CV, de l'analyser et de visualiser le résultat.
import React from "react";
import CVForm from "../components/CVForm";
import NLPPanel from "../components/NLPPanel";
import SkillsEvaluation from "../components/SkillsEvaluation";
import CVPreview from "../components/CVPreview";

const Dashboard = () => (
  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
    <div>
      <CVForm />
      <NLPPanel />
    </div>
    <div>
      <SkillsEvaluation />
      <CVPreview />
    </div>
  </div>
);

export default Dashboard;