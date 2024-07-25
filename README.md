<div align="center">
<img src="docs/logo.png" alt="Intelli-Talent" border="0" style="width: 35%; height: 35%;">
<h1/>
</div>

<div align="center">
    <h1 align='center'>⚡️<i>Intelli-Talent</i>⚡️</h1>
    <p><i>Get discovered. Get hired.</i></p>
</div>

<details open="open">
<summary>
<h2 style="display:inline">📝 Table of Contents</h2>
</summary>

- [⛏️ Built With](#built-with)
- [🏁 Getting started](#getting-started)
- [🏁 Description](#Description)
- [📷 Modules](#modules)
- [🏁 API Documentation](#API-Documentation)
- [✍️ Contributors](#contributors)
</details>

<hr>

<h2 href="#built-with">Built With : </h2>
 <ul>
  <li>Python</li>
  <li>Flask</li>
  <li>MongoDB</li>
  <li>RabbitMQ</li>
  <li>PyMongo</li>
  <li>Unittest</li>
 </ul>
<hr>

<h2 href="#getting-started">Getting Started</h2>
<blockquote>
  <p>This is a list of needed steps to set up your project locally, to get a local copy up and running follow these instructions.
 </p>
</blockquote>
<ol>
  <li><strong><em>Clone the repository</em></strong>
    <div>
        <code>$ git clone https://github.com/IntelliTalent/IntelliTalent-Flask.git</code>
    </div>
  </li>
  <li><strong><em>Navigate to project folder and create file named ".env"</em></strong>
    <div>
        <code>$ touch .env & cd IntelliTalent-Flask</code>
    </div>
  </li>
  <li><strong><em>Fill ".env" file with required fields</em></strong>
  </li>
  <li><strong><em>Install Docker and Docker Compose</em></strong>
  </li>
  <li><strong><em>Start all microservices</em></strong>
    <div>
        <code>$ docker compose up -d</code>
    </div>
  </li>

</ol>
<hr>

<h2  href="#Description">Description</h2>
<blockquote>
  <p>
  This platform was implemented for our Graduation Project by a team of 4 students.
  <br>
  <br>
  Intelli-Talent streamlines job searching and recruitment with features like automated CV and cover letter generation, job matching, and a Chrome extension for auto-filling application forms. For recruiters, it offers a comprehensive Application Tracking System (ATS) and multi-stage candidate filtration, including quizzes and interviews.
  <br>
  <br>
  This platform is developed with React js for the frontend, Nest.js for some backend services, and Flask for the other backend services.
 </p>
</blockquote>
<hr>
<h2 href="#API-Documentation">API Documentation</h2>
<blockquote>
  <p>
  You can look at the API documentation after running the nest.js application at <a href="http://localhost:3000/api/v1/docs#/">API Documentation</a>
  </p>
</blockquote>
<hr>

<h2 href="#modules">📷 Modules</h2>

<details>
<summary>
<h4 style="display:inline">
<strong><em>📝 Cover Letter Generator</em></strong></h4>
</summary>

- Validation and template selection based on word embedding similarity.
- Template filling and file uploading.

</details>

<details>
<summary>
<h4 style="display:inline">
<strong><em>📋 CV Generator </em></strong></h4>
</summary>

- Validation.
- Template filling and file uploading.

</details>

<details>
<summary>
<h4 style="display:inline">
<strong><em>💼 Custom Job Generator</em></strong></h4>
</summary>

- Extract common patterns from user job creation prompts.
- Generate structured jobs to be inserted into DB.

</details>

<details>
<summary>
<h4 style="display:inline">
<strong><em>📃 CV Extractor</em></strong></h4>
</summary>

- Extract multiple sections information from user CV, (education, experience, ...)
- Helps to easily create powerful profiles for users.

</details>

<details>
<summary>
<h4 style="display:inline">
<strong><em>👔 Job Extractor</em></strong></h4>
</summary>

- Extract information from unstrctured jobs (scraped from multiple channels, LinkedIn, Wuzzuf, ...).
- Genereate structured jobs to be inserted into DB.

</details>

<details>
<summary>
<h4 style="display:inline">
<strong><em>🔡 Quiz Generator</em></strong></h4>
</summary>

- Map wanted job skills into certain topics.
- Generate MCQ quizzes based on wanted topics.

</details>

<details>
<summary>
<h4 style="display:inline">
<strong><em>🔎 Scraper </em></strong></h4>
</summary>

- Periodically scrapes jobs from multiple channels, currently, LinkedIn & Wuzzuf.
- Periodically checks whether jobs are active/not active in all channels.

</details>

<h2 href="#Contributors">✍️ Contributors</h2>

<table>
<tr>
<td align="center">
<a href="https://github.com/Waer1" target="_black">
<img src="https://avatars.githubusercontent.com/u/70758177?v=4" width="150px;" alt="Waer1"/><br /><sub><b>Yousef Alwaer</b></sub></a><br />
</td>

<td align="center">
<a href="https://github.com/BeshoyMorad" target="_black">
<img src="https://avatars.githubusercontent.com/u/82404564?v=4" width="150px;" alt="BeshoyMorad"/><br /><sub><b>Beshoy Morad</b></sub></a><br />
</td>

<td align="center">
<a href="https://github.com/mohamednabilabdelfattah" target="_black">
<img src="https://avatars.githubusercontent.com/u/76039904?v=4" width="150px;" alt="Mohamed Nabil"/><br /><sub><b>Mohamed Nabil</b></sub></a><br />
</td>

<td align="center">
<a href="https://github.com/MoazHassan2022" target="_black">
<img src="https://avatars.githubusercontent.com/u/87096647?v=4" width="150px;" alt="Moaz Hassan"/><br /><sub><b>Moaz Hassan</b></sub></a><br />
</td>

</tr>
</table>
