const state = {
  jobs: [],
  eligibleOnly: true,
  query: "",
};

const els = {
  meta: document.getElementById("meta"),
  status: document.getElementById("status"),
  search: document.getElementById("search"),
  eligibleOnly: document.getElementById("eligible-only"),
  tbody: document.getElementById("job-table-body"),
  empty: document.getElementById("empty"),
};

function escapeHtml(value) {
  return String(value ?? "")
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

function formatDate(iso) {
  try {
    return new Date(iso).toLocaleString("ko-KR", {
      dateStyle: "medium",
      timeStyle: "short",
    });
  } catch {
    return iso;
  }
}

function render() {
  const query = state.query.trim().toLowerCase();

  const filtered = state.jobs.filter((job) => {
    if (state.eligibleOnly && !job.actually_eligible) return false;
    if (!query) return true;
    const haystack = `${job.title ?? ""} ${job.company ?? ""}`.toLowerCase();
    return haystack.includes(query);
  });

  els.tbody.innerHTML = filtered
    .map((job) => {
      const eligible = !!job.actually_eligible;
      const badge = eligible
        ? '<span class="badge ok">지원 가능</span>'
        : '<span class="badge no">지원 불가</span>';
      const reason =
        !eligible && job.exclude_reason
          ? `<span class="exclude-reason">${escapeHtml(job.exclude_reason)}</span>`
          : "";

      return `
        <tr>
          <td>
            <a class="job-link" href="${escapeHtml(job.url)}" target="_blank" rel="noopener">
              ${escapeHtml(job.title || "(제목 없음)")}
            </a>
          </td>
          <td>${escapeHtml(job.company || "-")}</td>
          <td>${escapeHtml(job.location || "-")}</td>
          <td>${escapeHtml(job.education || "-")}</td>
          <td>${escapeHtml(job.salary || "-")}</td>
          <td>${escapeHtml(job.posting_date || "-")}</td>
          <td>${badge}${reason}</td>
        </tr>
      `;
    })
    .join("");

  els.empty.hidden = filtered.length > 0;
}

function showStatus(message) {
  els.status.hidden = false;
  els.status.textContent = message;
}

async function init() {
  try {
    const res = await fetch("data/jobs.json", { cache: "no-store" });
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const data = await res.json();

    state.jobs = data.jobs || [];
    els.meta.textContent = `마지막 업데이트: ${formatDate(data.generated_at)} · 전체 ${data.total}건 중 지원 가능 ${data.eligible_total}건`;

    render();
  } catch (err) {
    showStatus(
      "아직 수집된 데이터가 없습니다. GitHub Actions 워크플로가 처음 실행되면 여기에 결과가 표시됩니다."
    );
    els.meta.textContent = "";
    console.error(err);
  }
}

els.search.addEventListener("input", (e) => {
  state.query = e.target.value;
  render();
});

els.eligibleOnly.addEventListener("change", (e) => {
  state.eligibleOnly = e.target.checked;
  render();
});

init();
