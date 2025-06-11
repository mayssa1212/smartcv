// =====================
// Fichier d'API centralisé pour SmartCV
// Toutes les fonctions d'accès à l'API backend (NLP, Auth, Users, CV, etc.)
// =====================

import { API_BASE_URL } from '../utils/constants';

// =====================
// --- MODULE AUTH ---
// =====================

// Connexion utilisateur
export async function login(email, password) {
  const response = await fetch(`${API_BASE_URL}/auth/login`, {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body: new URLSearchParams({
      username: email,
      password: password,
    }),
  });
  
  if (!response.ok) throw new Error("Erreur d'authentification");
  
  const data = await response.json();
  // Stocker le token dans localStorage pour persistance
  localStorage.setItem("token", data.access_token);
  return data;
}

// Déconnexion utilisateur
export function logoutUser() {
  localStorage.removeItem("token");
}

// Vérifier si l'utilisateur est connecté
export function isAuthenticated() {
  return localStorage.getItem("token") !== null;
}

// Récupérer le token d'authentification
export function getAuthToken() {
  return localStorage.getItem("token");
}

// Enregistrement d'un nouvel utilisateur
export async function register(email, password, fullName) {
  const response = await fetch(`${API_BASE_URL}/auth/register`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      email,
      password,
      full_name: fullName
    }),
  });
  
  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || "Erreur lors de l'inscription");
  }
  
  return await response.json();
}

// =====================
// --- MODULE NLP ---
// =====================

// Analyse NLP complète (langue, compétences, résumé, évaluation, expériences, diplômes)
export async function analyzeNLP(text) {
  const response = await fetch(`${API_BASE_URL}/nlp/analyze`, {
    method: "POST",
    headers: { 
      "Content-Type": "application/json",
      "Authorization": `Bearer ${getAuthToken()}`
    },
    body: JSON.stringify({ text }),
  });
  if (!response.ok) throw new Error("Erreur API NLP /analyze");
  return await response.json();
}

// Extraction des compétences (NLP)
export async function getNlpSkills(text) {
  const response = await fetch(`${API_BASE_URL}/nlp/skills`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text }),
  });
  if (!response.ok) throw new Error("Erreur API NLP /skills");
  return await response.json();
}

// Résumé automatique du texte (NLP)
export async function getNlpSummary(text) {
  const response = await fetch(`${API_BASE_URL}/nlp/summary`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text }),
  });
  if (!response.ok) throw new Error("Erreur API NLP /summary");
  return await response.json();
}

// Évaluation automatique du CV (NLP)
export async function getNlpEvaluation(text) {
  const response = await fetch(`${API_BASE_URL}/nlp/evaluate`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text }),
  });
  if (!response.ok) throw new Error("Erreur API NLP /evaluate");
  return await response.json();
}

// Détection de langue (NLP)
export async function getNlpLanguage(text) {
  const response = await fetch(`${API_BASE_URL}/nlp/language`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text }),
  });
  if (!response.ok) throw new Error("Erreur API NLP /language");
  return await response.json();
}

// Extraction des expériences professionnelles (NLP)
export async function getNlpExperiences(text) {
  const response = await fetch(`${API_BASE_URL}/nlp/experiences`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text }),
  });
  if (!response.ok) throw new Error("Erreur API NLP /experiences");
  return await response.json();
}

// Extraction des diplômes (NLP)
export async function getNlpDegrees(text) {
  const response = await fetch(`${API_BASE_URL}/nlp/degrees`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text }),
  });
  if (!response.ok) throw new Error("Erreur API NLP /degrees");
  return await response.json();
}

// =====================
// --- MODULE CV ---
// =====================

// Récupérer tous les CVs de l'utilisateur
export async function getUserCVs() {
  const response = await fetch(`${API_BASE_URL}/cvs`, {
    headers: { 
      "Authorization": `Bearer ${getAuthToken()}`
    }
  });
  if (!response.ok) throw new Error("Erreur lors de la récupération des CVs");
  return await response.json();
}

// Récupérer un CV spécifique
export async function getCV(id) {
  const response = await fetch(`${API_BASE_URL}/cvs/${id}`, {
    headers: { 
      "Authorization": `Bearer ${getAuthToken()}`
    }
  });
  if (!response.ok) throw new Error("Erreur lors de la récupération du CV");
  return await response.json();
}

// Créer un nouveau CV
export async function createCV(cvData) {
  const response = await fetch(`${API_BASE_URL}/cvs`, {
    method: "POST",
    headers: { 
      "Content-Type": "application/json",
      "Authorization": `Bearer ${getAuthToken()}`
    },
    body: JSON.stringify(cvData),
  });
  if (!response.ok) throw new Error("Erreur lors de la création du CV");
  return await response.json();
}

// Mettre à jour un CV existant
export async function updateCV(id, cvData) {
  const response = await fetch(`${API_BASE_URL}/cvs/${id}`, {
    method: "PUT",
    headers: { 
      "Content-Type": "application/json",
      "Authorization": `Bearer ${getAuthToken()}`
    },
    body: JSON.stringify(cvData),
  });
  if (!response.ok) throw new Error("Erreur lors de la mise à jour du CV");
  return await response.json();
}

// Supprimer un CV
export async function deleteCV(id) {
  const response = await fetch(`${API_BASE_URL}/cvs/${id}`, {
    method: "DELETE",
    headers: { 
      "Authorization": `Bearer ${getAuthToken()}`
    }
  });
  if (!response.ok) throw new Error("Erreur lors de la suppression du CV");
  return await response.json();
}

// =====================
// --- MODULE GENERATOR ---
// =====================

// Générer un CV en PDF
export async function generatePDF(cvId, template, colorTheme, font) {
  const response = await fetch(`${API_BASE_URL}/generator/generate-pdf`, {
    method: "POST",
    headers: { 
      "Content-Type": "application/json",
      "Authorization": `Bearer ${getAuthToken()}`
    },
    body: JSON.stringify({
      cv_id: cvId,
      template,
      color_theme: colorTheme,
      font
    }),
  });
  if (!response.ok) throw new Error("Erreur lors de la génération du PDF");
  return await response.json();
}

// Générer un CV en DOCX
export async function generateDOCX(cvId, template, colorTheme, font) {
  const response = await fetch(`${API_BASE_URL}/generator/generate-docx`, {
    method: "POST",
    headers: { 
      "Content-Type": "application/json",
      "Authorization": `Bearer ${getAuthToken()}`
    },
    body: JSON.stringify({
      cv_id: cvId,
      template,
      color_theme: colorTheme,
      font
    }),
  });
  if (!response.ok) throw new Error("Erreur lors de la génération du DOCX");
  return await response.json();
}

// Obtenir la liste des templates disponibles
export async function getAvailableTemplates() {
  const response = await fetch(`${API_BASE_URL}/generator/templates`, {
    method: "GET",
    headers: { 
      "Authorization": `Bearer ${getAuthToken()}`
    }
  });
  if (!response.ok) throw new Error("Erreur lors de la récupération des templates");
  return await response.json();
}

// =====================
// --- MODULE ASSISTANT ---
// =====================

// Obtenir des conseils du guide interactif
export async function getCVGuidance(text, jobTitle, step) {
  const response = await fetch(`${API_BASE_URL}/assistant/guide`, {
    method: "POST",
    headers: { 
      "Content-Type": "application/json",
      "Authorization": `Bearer ${getAuthToken()}`
    },
    body: JSON.stringify({
      text,
      job_title: jobTitle,
      step
    }),
  });
  if (!response.ok) throw new Error("Erreur lors de la récupération des conseils");
  return await response.json();
}
