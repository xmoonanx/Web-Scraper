const form = document.getElementById("search-form");
const resultsDiv = document.getElementById("results");
const loadingDiv = document.getElementById("loading");
const paginationDiv = document.getElementById("pagination");
let currentPage = 1;
let totalPages = 0;
const jobsPerPage = 6; // �������� ǥ���� ���� ��
let allJobs = [];

form.addEventListener("submit", async function (event) {
  event.preventDefault(); // �⺻ ���� ����
  const searchTerm = document.getElementById("search_term").value;

  loadingDiv.style.display = "block"; // �ε� ǥ��
  resultsDiv.style.display = "none"; // ���� ��� �����
  paginationDiv.style.display = "none"; // ���� ���������̼� �����

  const response = await fetch("/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ search_term: searchTerm }),
  });

  loadingDiv.style.display = "none"; // �ε� �����

  if (response.ok) {
    const data = await response.json();
    allJobs = data.jobs; // ��ü ��� ����
    currentPage = 1; // �������� �ʱ�ȭ
    totalPages = Math.ceil(allJobs.length / jobsPerPage); // �� ������ �� ���
    displayJobs(); // ��� ǥ��
    updatePagination(); // ���������̼� ������Ʈ
  } else {
    console.error("Error:", response.statusText); // ���� �α� �߰�
  }
});

function displayJobs() {
  resultsDiv.innerHTML = ""; // ��� �ʱ�ȭ
  const startIndex = (currentPage - 1) * jobsPerPage;
  const endIndex = startIndex + jobsPerPage;
  const jobsToDisplay = allJobs.slice(startIndex, endIndex);

  jobsToDisplay.forEach((job) => {
    const resultItem = document.createElement("div");
    resultItem.className = "result-item";
    resultItem.style.opacity = 1; // ��� ���� ����
    resultItem.innerHTML = `
            <div style="background-color: rgba(255, 255, 255, 0.1); padding: 10px; border-radius: 6px;">
                <strong>${job.title}</strong><br>
                ${job.company_name} - ${job.reward}<br>
                <a href="${job.link}" target="_blank">�ڼ��� ����</a>
            </div>
        `;
    resultsDiv.appendChild(resultItem);
  });

  resultsDiv.style.display = "grid"; // �׸���� ǥ��
}

function updatePagination() {
  paginationDiv.innerHTML = ""; // ���������̼� �ʱ�ȭ
  if (totalPages <= 1) return; // �������� �ϳ��̸� ���������̼� �����

  for (let i = 1; i <= totalPages; i++) {
    const button = document.createElement("button");
    button.innerText = i;
    button.disabled = i === currentPage; // ���� �������� ��Ȱ��ȭ
    button.addEventListener("click", () => {
      currentPage = i;
      displayJobs(); // ������ ������Ʈ
      updatePagination(); // ���������̼� ������Ʈ
    });
    paginationDiv.appendChild(button);
  }
  paginationDiv.style.display = "block"; // ���������̼� �����ֱ�
}
