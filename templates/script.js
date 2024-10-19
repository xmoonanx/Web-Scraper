const form = document.getElementById("search-form");
const resultsDiv = document.getElementById("results");
const loadingDiv = document.getElementById("loading");
const paginationDiv = document.getElementById("pagination");
let currentPage = 1;
let totalPages = 0;
const jobsPerPage = 6; // 페이지당 표시할 직업 수
let allJobs = [];

form.addEventListener("submit", async function (event) {
  event.preventDefault(); // 기본 제출 방지
  const searchTerm = document.getElementById("search_term").value;

  loadingDiv.style.display = "block"; // 로딩 표시
  resultsDiv.style.display = "none"; // 이전 결과 숨기기
  paginationDiv.style.display = "none"; // 이전 페이지네이션 숨기기

  const response = await fetch("/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ search_term: searchTerm }),
  });

  loadingDiv.style.display = "none"; // 로딩 숨기기

  if (response.ok) {
    const data = await response.json();
    allJobs = data.jobs; // 전체 결과 저장
    currentPage = 1; // 페이지를 초기화
    totalPages = Math.ceil(allJobs.length / jobsPerPage); // 총 페이지 수 계산
    displayJobs(); // 결과 표시
    updatePagination(); // 페이지네이션 업데이트
  } else {
    console.error("Error:", response.statusText); // 오류 로그 추가
  }
});

function displayJobs() {
  resultsDiv.innerHTML = ""; // 결과 초기화
  const startIndex = (currentPage - 1) * jobsPerPage;
  const endIndex = startIndex + jobsPerPage;
  const jobsToDisplay = allJobs.slice(startIndex, endIndex);

  jobsToDisplay.forEach((job) => {
    const resultItem = document.createElement("div");
    resultItem.className = "result-item";
    resultItem.style.opacity = 1; // 배경 투명도 설정
    resultItem.innerHTML = `
            <div style="background-color: rgba(255, 255, 255, 0.1); padding: 10px; border-radius: 6px;">
                <strong>${job.title}</strong><br>
                ${job.company_name} - ${job.reward}<br>
                <a href="${job.link}" target="_blank">자세히 보기</a>
            </div>
        `;
    resultsDiv.appendChild(resultItem);
  });

  resultsDiv.style.display = "grid"; // 그리드로 표시
}

function updatePagination() {
  paginationDiv.innerHTML = ""; // 페이지네이션 초기화
  if (totalPages <= 1) return; // 페이지가 하나이면 페이지네이션 숨기기

  for (let i = 1; i <= totalPages; i++) {
    const button = document.createElement("button");
    button.innerText = i;
    button.disabled = i === currentPage; // 현재 페이지는 비활성화
    button.addEventListener("click", () => {
      currentPage = i;
      displayJobs(); // 페이지 업데이트
      updatePagination(); // 페이지네이션 업데이트
    });
    paginationDiv.appendChild(button);
  }
  paginationDiv.style.display = "block"; // 페이지네이션 보여주기
}
