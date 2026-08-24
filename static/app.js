const $ = id => document.getElementById(id);

async function get(url) {
    const r = await fetch(url);
    const d = await r.json();

    if (!r.ok) {
        throw new Error(d.error || d.message || "Request failed");
    }

    return d;
}

async function health() {
    try {
        await get("/api/health");
        $("status").textContent = "● CognoDB connected";
    } catch (e) {
        $("status").textContent = "● Database unavailable";
    }
}

async function searchMovies() {
    const q = $("search").value.trim();

    if (!q) {
        return;
    }

    $("results").innerHTML =
        '<div class="empty">Searching graph...</div>';

    try {
        const rows = await get(
            "/api/movies?q=" + encodeURIComponent(q)
        );

        $("resultCount").textContent =
            rows.length + " matches";

        if (!rows.length) {
            $("results").innerHTML =
                '<div class="empty">No matching movies.</div>';
            return;
        }

        $("results").innerHTML = "";

        rows.forEach(movie => {
            const card = document.createElement("div");
            card.className = "card";

            const genres = (movie.genres || [])
                .map(g => `<span class="pill">${esc(g)}</span>`)
                .join("");

            card.innerHTML = `
                <h3>${esc(movie.title)}</h3>
                <div class="meta">
                    ${movie.year} · Rating ${movie.rating}
                </div>
                <div>
                    ${genres}
                </div>
            `;

            // Attach click event directly
            card.addEventListener("click", () => {
                selectMovie(movie.title);
            });

            $("results").appendChild(card);
        });

    } catch (e) {
        $("results").innerHTML =
            '<div class="empty">' + esc(e.message) + "</div>";
    }
}


async function selectMovie(title) {
    $("details").innerHTML =
        '<div class="empty">Loading graph neighborhood...</div>';

    try {
        const [d, recs, two] = await Promise.all([
            get("/api/movie/" + encodeURIComponent(title)),
            get(
                "/api/recommendations?title=" +
                encodeURIComponent(title)
            ),
            get(
                "/api/two-hop?title=" +
                encodeURIComponent(title)
            )
        ]);

        $("details").innerHTML = `
            <h3>${esc(d.title)}</h3>

            <div class="detailrow">
                <div class="label">Year / Rating</div>
                <div class="value">
                    ${d.year} · ${d.rating}
                </div>
            </div>

            <div class="detailrow">
                <div class="label">Genres</div>
                <div class="value">
                    ${(d.genres || [])
                        .map(g => esc(g))
                        .join(", ")}
                </div>
            </div>

            <div class="detailrow">
                <div class="label">Actors</div>
                <div class="value">
                    ${(d.actors || [])
                        .map(a => esc(a))
                        .join(", ")}
                </div>
            </div>

            <div class="detailrow">
                <div class="label">Directors</div>
                <div class="value">
                    ${(d.directors || [])
                        .map(x => esc(x))
                        .join(", ")}
                </div>
            </div>

            <div class="detailrow">
                <div class="label">
                    Recommended via shared graph connections
                </div>

                <div class="value">
                    ${
                        recs
                            .map(
                                r =>
                                    `${esc(r.title)} (${r.sharedActors} shared actors)`
                            )
                            .join("<br>") || "None"
                    }
                </div>
            </div>

            <div class="detailrow">
                <div class="label">
                    2-hop discovery
                </div>

                <div class="value">
                    ${
                        two
                            .map(
                                r =>
                                    `${esc(r.title)} (${r.secondHopActors} second-hop actors)`
                            )
                            .join("<br>") || "None"
                    }
                </div>
            </div>
        `;

    } catch (e) {
        $("details").innerHTML =
            '<div class="empty">' +
            esc(e.message) +
            "</div>";
    }
}


async function loadGenres() {
    try {
        const rows = await get("/api/genres");

        $("genres").innerHTML = rows
            .map(
                r => `
                    <div class="genre">
                        <strong>${esc(r.genre)}</strong>
                        <span>
                            ${r.movies} movies ·
                            ${r.avgRating} avg rating
                        </span>
                    </div>
                `
            )
            .join("");

    } catch (e) {
        $("genres").innerHTML =
            '<div class="empty">' +
            esc(e.message) +
            "</div>";
    }
}


function esc(s) {
    return String(s ?? "").replace(
        /[&<>'"]/g,
        c =>
            ({
                "&": "&amp;",
                "<": "&lt;",
                ">": "&gt;",
                "'": "&#39;",
                '"': "&quot;"
            })[c]
    );
}


$("search").addEventListener("keydown", e => {
    if (e.key === "Enter") {
        searchMovies();
    }
});


health();
loadGenres();