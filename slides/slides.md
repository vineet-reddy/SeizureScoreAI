---
theme: seriph
background: https://images.unsplash.com/photo-1559757175-5700dde675bc?w=1920
title: 'SeizureScoreAI: Multi-Agent Clinical Reasoning'
info: |
  A multi-agent system that emulates epileptologist decision-making for ILAE outcome scoring.
  
  Slides template adapted from [google-gemini/workshops](https://github.com/google-gemini/workshops/tree/main/startupcon/slides)
transition: slide-left
mdc: true
---

# SeizureScoreAI

<v-clicks>

## Teaching LLMs to Reason Like Epileptologists

Vineet Reddy

</v-clicks>

---

# What is Epilepsy?

<div class="grid grid-cols-2 gap-8 items-center h-full">
<div v-click class="flex flex-col gap-4 justify-center">

> **50 million** people worldwide have epilepsy.
>
> **Seizures** are caused by abnormal electrical activity in the brain.
>
> **Surgery** can eliminate seizures in 60-70% of patients - but how do we measure success?

</div>
<div v-click class="flex items-center justify-center">
<img src="https://i.makeagif.com/media/5-16-2017/Uud6Cg.gif" class="rounded-lg shadow-lg max-h-[40vh]" alt="Types of seizures" />
</div>
</div>

<!-- Epilepsy is a neurological disorder. After surgery, clinicians need a standardized way to measure outcomes. -->

---

# The ILAE Outcome Scale

<div class="grid grid-cols-2 gap-8 items-center h-full">
<div v-click class="flex flex-col gap-4 justify-center text-sm">

| Class | Outcome |
|-------|---------|
| **1** | Seizure-free, no auras |
| **2** | Only auras, no seizures |
| **3** | 1-3 seizure days/year |
| **4** | 4+ days to 50% reduction |
| **5** | Less than 50% reduction |
| **6** | More than 100% increase |

</div>
<div v-click class="flex flex-col gap-4 justify-center">

> **The Problem:**
>
> Calculating ILAE scores requires:
> - Reading dense clinical notes
> - Extracting seizure frequencies
> - Comparing pre/post surgery status
> - Applying classification rules
>
> **Can an LLM do this?**

</div>
</div>

<!-- ILAE = International League Against Epilepsy. Gold standard for measuring surgical outcomes. -->

---

# Architecture: 3 Agents, 1 Pipeline

<div class="flex flex-col items-center justify-center h-full gap-4">
<div v-click class="flex items-center gap-3 text-sm">
  <div class="px-3 py-2 bg-sky-100 border-2 border-sky-500 rounded-lg text-center min-w-[120px]">
    <div class="font-bold">Clinical Note</div>
    <div class="text-xs text-gray-600">Raw text input</div>
  </div>
  <span class="text-2xl">→</span>
  <div class="px-3 py-2 bg-amber-100 border-2 border-amber-500 rounded-lg text-center min-w-[140px]">
    <div class="font-bold">Agent 1: Extractor</div>
    <div class="text-xs text-gray-600">Extracts seizure freedom,</div>
    <div class="text-xs text-gray-600">auras, frequencies</div>
  </div>
  <span class="text-2xl">→</span>
  <div class="px-3 py-2 bg-pink-100 border-2 border-pink-500 rounded-lg text-center min-w-[140px]">
    <div class="font-bold">Agent 2: Calculator</div>
    <div class="text-xs text-gray-600">Applies ILAE criteria,</div>
    <div class="text-xs text-gray-600">computes score</div>
  </div>
  <span class="text-2xl">→</span>
  <div class="px-3 py-2 bg-emerald-100 border-2 border-emerald-500 rounded-lg text-center min-w-[140px]">
    <div class="font-bold">Agent 3: Reporter</div>
    <div class="text-xs text-gray-600">Generates concise</div>
    <div class="text-xs text-gray-600">explanation</div>
  </div>
  <span class="text-2xl">→</span>
  <div class="px-3 py-2 bg-sky-100 border-2 border-sky-500 rounded-lg text-center min-w-[100px]">
    <div class="font-bold">ILAE Score</div>
    <div class="text-xs text-gray-600">1-6 or indeterminate</div>
  </div>
</div>

<div v-click class="text-center mt-6 text-sm">

> Built with **Google ADK** (Agent Development Kit) + **Gemini 3 Flash**
>
> Each agent is an `LlmAgent` with a focused instruction → JSON handoffs → reliable outputs

</div>
</div>

<!-- Google's Agent Development Kit handles session management and agent orchestration. -->

---

# Demo

<div class="flex flex-col items-center justify-center h-full gap-4">
<div v-click class="text-center">

<iframe width="560" height="315" src="https://www.youtube.com/embed/YOUR_VIDEO_ID" frameborder="0" allowfullscreen class="rounded-lg shadow-lg"></iframe>

</div>
<div v-click class="text-center mt-4">

> **Try it:** Upload a clinical note → Get ILAE score + explanation
>
> [github.com/vineet-reddy/SeizureScoreAI](https://github.com/vineet-reddy/SeizureScoreAI)

</div>
</div>

<!-- Replace YOUR_VIDEO_ID in the iframe src with your actual YouTube video ID -->
