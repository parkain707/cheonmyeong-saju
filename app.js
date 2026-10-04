// ==========================================================================
// 天命明鏡 (천명명경) | 현허도인의 천기 신점사주 클라이언트 애플리케이션 (세계 영성 융합 & VIP 과금 엔진)
// ==========================================================================

document.addEventListener("DOMContentLoaded", () => {
    // 100% 원클릭 칩 상태 변수
    let selectedGender = "male";
    let selectedAnimal = "닭";
    let selectedYear = 1993;
    let selectedCalendar = "solar";
    let isLeap = false;
    let selectedMonth = 8;
    let selectedDay = 17;
    let selectedHour = 18;
    let selectedConcern = "career";
    let selectedFlag = "황";

    // 폼 요소
    const sajuForm = document.getElementById("saju-form");
    const dayRange = document.getElementById("day-range");
    const selectedDayLabel = document.getElementById("selected-day-label");
    const yearChipsContainer = document.getElementById("year-chips-container");
    
    // 섹션 요소
    const inputSection = document.getElementById("input-section");
    const loadingOverlay = document.getElementById("loading-overlay");
    const loadingText = document.getElementById("loading-text");
    const resultSection = document.getElementById("result-section");
    const correctionBanner = document.getElementById("correction-banner");
    const correctionNotes = document.getElementById("correction-notes");
    
    // 페이월 & 부적 모달 요소
    const paywallModal = document.getElementById("paywall-modal");
    const modalCloseBtn = document.getElementById("modal-close-btn");
    const openPaywallBtn = document.getElementById("open-paywall-btn");
    const simulatePayBtn = document.getElementById("simulate-pay-btn");
    const amuletModal = document.getElementById("amulet-modal");
    const amuletCloseBtn = document.getElementById("amulet-close-btn");
    const downloadAmuletBtn = document.getElementById("download-amulet-btn");
    const saveCanvasBtn = document.getElementById("save-canvas-btn");
    const amuletCanvas = document.getElementById("amulet-canvas");

    // 버튼 & 상호작용
    const copySummaryBtn = document.getElementById("copy-summary-btn");
    const submitBtn = sajuForm ? sajuForm.querySelector(".submit-btn") : null;

    let chaptersData = [];
    let isVipUnlocked = false;
    let cachedSaju = null;
    let cachedReading = null;
    let cachedSpirit = null;
    let cachedGlobal = null;
    let cachedZiwei = null;
    let currentUserName = "자네";

    // 0. 모바일 PWA 서비스 워커 등록
    if ("serviceWorker" in navigator) {
        window.addEventListener("load", () => {
            navigator.serviceWorker.register("/sw.js").catch(() => {});
        });
    }

    // 모바일 햅틱(진동) 피드백 헬퍼
    function triggerHaptic(ms = 22) {
        if ("vibrate" in navigator) {
            try { navigator.vibrate(ms); } catch (e) {}
        }
    }

    // 1. 성별 칩 클릭
    const genderChips = document.querySelectorAll('.select-chip[data-group="gender"]');
    genderChips.forEach(chip => {
        chip.addEventListener("click", () => {
            triggerHaptic(18);
            genderChips.forEach(c => c.classList.remove("active"));
            chip.classList.add("active");
            selectedGender = chip.dataset.value;
        });
    });

    // 2. 12간지 띠 & 연대 원클릭 동적 연동 (내림차순 정렬 & 완벽 양방향)
    const currentYear = new Date().getFullYear();
    const zodiacChips = document.querySelectorAll(".zodiac-chip");
    const decadeChips = document.querySelectorAll(".decade-chip");
    const selectedYearSummary = document.getElementById("selected-year-summary");
    const ZODIAC_ANIMALS = ["원숭이", "닭", "개", "돼지", "쥐", "소", "호랑이", "토끼", "용", "뱀", "말", "양"];

    function getZodiacForYear(yr) {
        return ZODIAC_ANIMALS[yr % 12];
    }

    function updateYearSummary(yr) {
        const age = currentYear - yr + 1;
        const animal = getZodiacForYear(yr);
        selectedYear = yr;
        selectedAnimal = animal;
        if (selectedYearSummary) {
            selectedYearSummary.textContent = `${yr}년생 (${animal}띠, ${age}세)`;
        }
        // 12간지 칩 자동 하이라이트 동기화
        zodiacChips.forEach(chip => {
            if (chip.dataset.animal === animal) {
                chip.classList.add("active");
            } else {
                chip.classList.remove("active");
            }
        });
    }

    function renderYearChips(yearsArray, preselectYear) {
        // 무조건 최신순(내림차순) 정렬: 예) 2016 -> 2004 -> 1992 -> 1980 -> 1968...
        const sortedYears = [...yearsArray].sort((a, b) => b - a);
        yearChipsContainer.innerHTML = "";

        // 기본 선택 연도 (전달받은 연도이거나, 1980~1995 사이의 성인 주 연령층 우선)
        let targetSelected = preselectYear;
        if (!targetSelected) {
            targetSelected = sortedYears.find(y => y <= 2004 && y >= 1970) || sortedYears[0];
        }

        sortedYears.forEach(yr => {
            const age = currentYear - yr + 1;
            const btn = document.createElement("button");
            btn.type = "button";
            btn.className = `select-chip ${yr === targetSelected ? "active" : ""}`;
            btn.dataset.group = "year";
            btn.dataset.value = yr;
            btn.textContent = `${yr}년 (${age}세)`;

            btn.addEventListener("click", () => {
                yearChipsContainer.querySelectorAll(".select-chip").forEach(c => c.classList.remove("active"));
                btn.classList.add("active");
                updateYearSummary(yr);
            });

            yearChipsContainer.appendChild(btn);
        });

        updateYearSummary(targetSelected);
    }

    // 12간지 띠 칩 클릭 시
    zodiacChips.forEach(chip => {
        chip.addEventListener("click", () => {
            zodiacChips.forEach(c => c.classList.remove("active"));
            decadeChips.forEach(c => c.classList.remove("active"));
            chip.classList.add("active");

            const yearsStr = chip.dataset.years;
            const years = yearsStr.split(",").map(y => parseInt(y.trim()));
            renderYearChips(years);
        });
    });

    // 빠른 연대 칩 클릭 시 (90년대, 80년대, 70년대 등)
    decadeChips.forEach(chip => {
        chip.addEventListener("click", () => {
            decadeChips.forEach(c => c.classList.remove("active"));
            chip.classList.add("active");

            const decade = parseInt(chip.dataset.decade);
            let years = [];
            if (decade === 2000) {
                for (let y = 2015; y >= 2000; y--) years.push(y);
            } else if (decade === 1950) {
                for (let y = 1959; y >= 1944; y--) years.push(y);
            } else {
                for (let y = decade + 9; y >= decade; y--) years.push(y);
            }
            renderYearChips(years);
        });
    });

    // 초기 상태 세팅 (1993년 닭띠)
    updateYearSummary(1993);

    // 3. 달력 구분 칩
    const calChips = document.querySelectorAll('.select-chip[data-group="calendar"]');
    calChips.forEach(chip => {
        chip.addEventListener("click", () => {
            calChips.forEach(c => c.classList.remove("active"));
            chip.classList.add("active");
            const val = chip.dataset.value;
            if (val === "solar") {
                selectedCalendar = "solar";
                isLeap = false;
            } else if (val === "lunar") {
                selectedCalendar = "lunar";
                isLeap = false;
            } else if (val === "lunar_leap") {
                selectedCalendar = "lunar";
                isLeap = true;
            }
        });
    });

    // 4. 출생월 칩
    const monthChips = document.querySelectorAll('.select-chip[data-group="month"]');
    monthChips.forEach(chip => {
        chip.addEventListener("click", () => {
            triggerHaptic(18);
            monthChips.forEach(c => c.classList.remove("active"));
            chip.classList.add("active");
            selectedMonth = parseInt(chip.dataset.value);
        });
    });

    // 5. 출생일 슬라이더
    if (dayRange && selectedDayLabel) {
        dayRange.addEventListener("input", (e) => {
            selectedDay = parseInt(e.target.value);
            selectedDayLabel.textContent = `${selectedDay}일`;
        });
    }

    // 6. 태어난 시간대 칩
    const timeChips = document.querySelectorAll(".time-chip");
    timeChips.forEach(chip => {
        chip.addEventListener("click", () => {
            triggerHaptic(20);
            timeChips.forEach(c => c.classList.remove("active"));
            chip.classList.add("active");
            selectedHour = parseInt(chip.dataset.hour);
        });
    });

    // 7. 고민 칩
    const concernChips = document.querySelectorAll('.select-chip[data-group="concern"]');
    concernChips.forEach(chip => {
        chip.addEventListener("click", () => {
            triggerHaptic(22);
            concernChips.forEach(c => c.classList.remove("active"));
            chip.classList.add("active");
            selectedConcern = chip.dataset.value;
        });
    });

    // 8. 오방기 깃발 선택 이벤트
    const flagBtns = document.querySelectorAll(".obanggi-flag");
    flagBtns.forEach(btn => {
        btn.addEventListener("click", () => {
            triggerHaptic(30);
            flagBtns.forEach(b => b.classList.remove("active"));
            btn.classList.add("active");
            selectedFlag = btn.dataset.flag;
        });
    });

    // 토스트 알림 헬퍼
    function showToast(msg) {
        const container = document.getElementById("toast-container");
        if (!container) return;
        const toast = document.createElement("div");
        toast.className = "toast";
        toast.textContent = msg;
        container.appendChild(toast);
        setTimeout(() => {
            if (toast.parentNode) toast.parentNode.removeChild(toast);
        }, 3000);
    }

    // 폼 제출 이벤트
    sajuForm.addEventListener("submit", async (e) => {
        e.preventDefault();

        if (submitBtn) {
            submitBtn.disabled = true;
            submitBtn.style.opacity = "0.6";
            submitBtn.style.pointerEvents = "none";
        }

        currentUserName = "귀하";

        // Soul Memory: 이전 방문 기록 읽기 (localStorage)
        let prevVisit = null;
        try {
            const stored = localStorage.getItem("soul_memory");
            if (stored) prevVisit = JSON.parse(stored);
        } catch (e) { /* 첫 방문 */ }

        let requestBody = {
            name: currentUserName,
            gender: selectedGender,
            obanggi: selectedFlag,
            year: selectedYear,
            month: selectedMonth,
            day: selectedDay,
            hour: selectedHour,
            calendar_type: selectedCalendar,
            is_leap: isLeap,
            concern: selectedConcern,
            is_unlocked: isVipUnlocked,
            prev_visit: prevVisit
        };

        showLoading();

        try {
            const resp = await fetch("/api/saju", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(requestBody)
            });

            if (!resp.ok) {
                const errData = await resp.json().catch(() => ({}));
                throw new Error(errData.message || "사주 계산 중 서버 오류가 발생했습니다.");
            }

            const data = await resp.json();
            if (data.status !== "success") throw new Error(data.message || "사주 풀이에 실패했습니다.");

            cachedSaju = data.saju;
            cachedReading = data.reading;
            cachedSpirit = data.spirit_vision;
            cachedGlobal = data.global_spirit;
            cachedZiwei = data.ziwei;

            // Soul Memory: 이번 방문 기록을 localStorage에 저장
            try {
                const now = new Date();
                const soulMemory = {
                    timestamp: `${now.getFullYear()}년 ${now.getMonth() + 1}월 ${now.getDate()}일`,
                    concern: selectedConcern,
                    obanggi: selectedFlag,
                    year: selectedYear,
                    month: selectedMonth,
                    day: selectedDay,
                    hour: selectedHour
                };
                localStorage.setItem("soul_memory", JSON.stringify(soulMemory));
            } catch (e) { /* localStorage 미지원 환경 무시 */ }

            setTimeout(() => {
                try {
                    renderResult(
                        data.saju,
                        data.reading,
                        data.notes,
                        data.spirit_vision,
                        data.global_spirit,
                        data.ziwei,
                        data.destiny_partners,
                        data.destiny_place,
                        data.lantern_fortune,
                        data.caution_calendar,
                        data.mz_insight
                    );
                } catch (renderErr) {
                    console.error("렌더링 오류 감지 (결과창 강제 노출):", renderErr);
                } finally {
                    hideLoading();
                    if (submitBtn) {
                        submitBtn.disabled = false;
                        submitBtn.style.opacity = "1";
                        submitBtn.style.pointerEvents = "auto";
                    }
                }
            }, 600);

        } catch (err) {
            hideLoading();
            if (submitBtn) {
                submitBtn.disabled = false;
                submitBtn.style.opacity = "1";
                submitBtn.style.pointerEvents = "auto";
            }
            showToast("⚠️ " + err.message);
        }
    });

    function showLoading() {
        loadingOverlay.classList.remove("hidden");
        loadingText.textContent = "하늘의 신령한 기운과 주파수를 조율 중입니다...";
        setTimeout(() => {
            if (!loadingOverlay.classList.contains("hidden")) {
                const sub = document.querySelector(".loading-sub");
                if (sub) sub.textContent = "현허도인의 깊은 혜안으로 그대의 타고난 천명과 황금기 운세를 살피고 있습니다.";
            }
        }, 600);
    }

    function hideLoading() {
        loadingOverlay.classList.add("hidden");
        inputSection.classList.add("hidden");
        resultSection.classList.remove("hidden");
        window.scrollTo({ top: 0, behavior: 'smooth' });
    }

    // 안전한 DOM 텍스트/HTML 설정 헬퍼
    function safeSetText(id, text) {
        const el = document.getElementById(id);
        if (el) el.textContent = (text !== undefined && text !== null) ? text : "";
    }
    function safeSetHtml(id, html) {
        const el = document.getElementById(id);
        if (el) el.innerHTML = (html !== undefined && html !== null) ? html : "";
    }

    function formatMarkdown(text) {
        if (!text) return "";
        return text
            .replace(/\*\*(.*?)\*\*/g, '<strong style="color:var(--gold-light); font-weight:800;">$1</strong>')
            .replace(/\n\n/g, '<br><br>')
            .replace(/\n/g, '<br>');
    }

    // 결과 렌더링
    function renderResult(saju, reading, notes, spiritVision, globalSpirit, ziwei, destinyPartners, destinyPlace, lanternFortune, cautionCalendar, mzInsight) {
        // 0. 스마트 보정 알림
        if (notes && notes.length > 0) {
            correctionBanner.classList.remove("hidden");
            correctionNotes.innerHTML = notes.map(n => `<li>${n}</li>`).join("");
        } else {
            correctionBanner.classList.add("hidden");
        }

        // 0-0. [2030 바이럴 킬러] 천명 페르소나 스펙 카드 & 현실 팩폭관 렌더링
        if (mzInsight && saju) {
            renderMzSpecCard(saju, mzInsight);
            renderMzRealityLab(mzInsight);
        }

        // 0-1. [2030 혁신] 도인의 웹툰 시네마틱 옴니버스 리포트 렌더링 & 기본 웹툰 뷰 설정
        renderWebtoonReport(saju, spiritVision, lanternFortune, destinyPartners, destinyPlace, cautionCalendar, mzInsight);
        switchResultView("webtoon");

        // 0-1. 청월당 4대 킬러 출력 포맷 렌더링 (정밀 뷰 데이터 동기화)
        if (lanternFortune) renderLanternFortune(lanternFortune);
        if (cautionCalendar) renderCautionCalendar(cautionCalendar);
        if (destinyPartners) renderDestinyPartners(destinyPartners);
        if (destinyPlace) renderDestinyPlace(destinyPlace);

        // 1. 신점 영안 투시 카드
        if (spiritVision) {
            safeSetText("res-spirit-moment", (spiritVision.moment_timestamp || "") + " 영동(靈動)");
            safeSetText("res-spirit-name", spiritVision.spirit_name);
            safeSetText("res-spirit-desc", spiritVision.spirit_desc);
            safeSetHtml("res-shamanic-speech", formatMarkdown(spiritVision.shamanic_speech));
            if (spiritVision.obanggi) {
                safeSetText("res-obanggi-oracle", `[${spiritVision.obanggi.color}] ${spiritVision.obanggi.oracle}`);
            }

            // 공시성(Synchronicity) 실시간 천문 데이터 표시
            if (spiritVision.synchronicity) {
                const sync = spiritVision.synchronicity;
                const syncEl = document.getElementById("res-synchronicity-moment");
                if (syncEl) {
                    const shijinText = sync.shijin ? `${sync.shijin.name} ${sync.shijin.gak}` : "";
                    const lunarText = sync.lunar ? sync.lunar.title : "";
                    syncEl.innerHTML = `<span class="sync-shijin">🕐 ${shijinText}</span> · <span class="sync-lunar">🌙 ${lunarText}</span>`;
                }
            }

            // 무의식 그림자(Shadow Archetype) 표시
            if (spiritVision.unconscious_shadow) {
                const shadow = spiritVision.unconscious_shadow;
                const shadowEl = document.getElementById("res-unconscious-shadow");
                if (shadowEl) {
                    shadowEl.innerHTML = `<div class="shadow-archetype-card"><div class="shadow-type">🪞 ${shadow.type}</div><div class="shadow-insight">${shadow.insight}</div></div>`;
                }
            }

            // 재방문자 표시
            if (spiritVision.is_reunion) {
                const reunionEl = document.getElementById("res-reunion-badge");
                if (reunionEl) {
                    reunionEl.classList.remove("hidden");
                    reunionEl.textContent = "🔮 재방문 영혼 — 도인이 그대를 기억하고 있소";
                }
            }
        }

        // 2. 세계 영성 (융 원형, 차크라, 주역, 일일신점, 부적)
        if (globalSpirit) {
            safeSetText("res-daily-fortune", globalSpirit.daily_fortune);
            
            // 칼 융
            if (globalSpirit.archetype) {
                safeSetText("res-archetype-tag", (globalSpirit.archetype.title || "").split(" ")[0]);
                safeSetText("res-archetype-title", globalSpirit.archetype.title);
                safeSetText("res-archetype-desc", globalSpirit.archetype.light);
            }
            if (globalSpirit.shadow) {
                safeSetText("res-shadow-desc", `${globalSpirit.shadow.title} — ${globalSpirit.shadow.desc}`);
            }

            // 차크라 & 오라
            if (globalSpirit.aura) {
                safeSetText("res-aura-tag", (globalSpirit.aura.name || "").split(" ")[0]);
                safeSetText("res-aura-title", globalSpirit.aura.name);
                safeSetText("res-aura-desc", globalSpirit.aura.desc);
            }
            const chakraList = document.getElementById("res-chakra-list");
            if (chakraList && globalSpirit.chakras) {
                chakraList.innerHTML = globalSpirit.chakras.slice(0, 4).map(c => `
                    <div class="chakra-item">
                        <span>${c.name}</span>
                        <span class="chakra-status">${c.status}</span>
                    </div>
                `).join("");
            }

            // 주역 64괘
            if (globalSpirit.iching) {
                safeSetText("res-iching-tag", (globalSpirit.iching.hexagram || "").split(" ")[0]);
                safeSetText("res-iching-title", globalSpirit.iching.hexagram);
                safeSetText("res-iching-desc", globalSpirit.iching.meaning);
            }

            // 부적 정보
            if (globalSpirit.amulet) {
                safeSetText("res-amulet-title", globalSpirit.amulet.name);
                safeSetText("res-amulet-desc", globalSpirit.amulet.desc);
                safeSetText("res-amulet-name", (globalSpirit.amulet.name || "").slice(0, 6));
            }
        }

        // 3. 만세력 명식표
        if (reading) {
            safeSetText("res-preview-text", reading.preview_text);
        }
        if (saju && saju.pillars) {
            const p = saju.pillars;
            const hourHeader = document.getElementById("hour-header-label");
            if (hourHeader) {
                hourHeader.innerHTML = saju.time_estimated ? `시주 (時柱) <span style="font-size:0.75rem; color:#f39c12; font-weight:normal;">[역추론]</span>` : "시주 (時柱)";
            }

            renderPillarCell("res-hour", p.hour);
            renderPillarCell("res-day", p.day);
            renderPillarCell("res-month", p.month);
            renderPillarCell("res-year", p.year);

            if (saju.oheng_counts) {
                const oc = saju.oheng_counts;
                safeSetText("o-wood-cnt", (oc["목"] || 0) + "개");
                safeSetText("o-fire-cnt", (oc["화"] || 0) + "개");
                safeSetText("o-earth-cnt", (oc["토"] || 0) + "개");
                safeSetText("o-metal-cnt", (oc["금"] || 0) + "개");
                safeSetText("o-water-cnt", (oc["수"] || 0) + "개");
            }

            // 4. 육감 차트 & 4대 문
            if (saju.six_senses) renderRadarChart(saju.six_senses);
            if (saju.gates) renderGates(saju.gates);
            // 4.5 황실 비전 자미두수 12궁 성반
            if (ziwei) renderZiweiChart(ziwei);
        }

        // 5. 11개 챕터 풀이 (잠금/해제 처리)
        if (reading && reading.sections) {
            chaptersData = reading.sections;
            renderChapters("all");
        }

        // VIP 배너 표시 상태
        const paywallBanner = document.getElementById("vip-paywall-banner");
        if (paywallBanner) {
            paywallBanner.style.display = isVipUnlocked ? "none" : "block";
        }
    }

    // 황실 비전 자미두수 12궁 성반 렌더링
    function renderZiweiChart(zw) {
        if (!zw) return;

        // 요약 바
        safeSetText("zw-bureau", zw.bureau ? zw.bureau.name : "-");
        safeSetText("zw-ming-loc", zw.ming_palace ? `${zw.ming_palace.ji_hanja}궁 (${zw.ming_palace.ji})` : "-");
        
        const mStars = (zw.ming_palace && zw.ming_palace.stars && zw.ming_palace.stars.length > 0)
            ? zw.ming_palace.stars.map(s => s.name).join("·")
            : "명궁 무주성 (천이궁 차용)";
        safeSetText("zw-ming-stars", mStars);
        
        safeSetText("zw-shen-loc", zw.shen_palace ? `${zw.shen_palace.ji_hanja}궁 (${zw.shen_palace.ji})` : "-");

        const hwayiPalace = (zw.sihua && zw.sihua.기) ? zw.sihua.기.palace : "-";
        const hwayiStar = (zw.sihua && zw.sihua.기) ? zw.sihua.기.star : "";
        safeSetText("zw-hwayi-loc", `${hwayiPalace} (${hwayiStar}化忌)`);

        // 도인의 천기 직설
        safeSetHtml("zw-oracle-text", formatMarkdown(zw.oracle_summary));

        // 12궁 성반 그리드
        const grid = document.getElementById("zw-palaces-grid");
        if (!grid || !zw.palaces) return;
        grid.innerHTML = "";

        const palaceKeys = [
            "명궁", "형제궁", "부처궁", "자녀궁",
            "재백궁", "질액궁", "천이궁", "노복궁",
            "관록궁", "전택궁", "복덕궁", "부모궁"
        ];

        palaceKeys.forEach(pName => {
            const p = zw.palaces[pName];
            if (!p) return;

            const isMing = (pName === "명궁");
            const hasHwayi = (pName === hwayiPalace);
            const card = document.createElement("div");
            card.className = `zw-palace-card ${isMing ? "is-ming" : ""} ${hasHwayi ? "has-hwayi" : ""}`;

            // 주성 뱃지들
            let starsHtml = "";
            if (p.stars && p.stars.length > 0) {
                starsHtml = p.stars.map(s => {
                    const isEmperor = ["자미", "천부", "칠살", "태양"].includes(s.name);
                    return `<span class="zw-star-badge ${isEmperor ? "zw-emperor" : ""}" title="${s.desc}">${s.name}(${s.hanja})</span>`;
                }).join("");
            } else {
                starsHtml = `<span class="zw-star-empty">비어있음 (대궁 차용)</span>`;
            }

            // 사화 태그들
            let sihuaHtml = "";
            if (p.sihua && p.sihua.length > 0) {
                sihuaHtml = p.sihua.map(sh => {
                    let shClass = "sh-록";
                    if (sh.includes("化權")) shClass = "sh-권";
                    else if (sh.includes("化科")) shClass = "sh-과";
                    else if (sh.includes("化忌")) shClass = "sh-기";
                    return `<span class="sihua-tag ${shClass}">${sh}</span>`;
                }).join("");
            }

            card.innerHTML = `
                <div class="zw-p-header">
                    <span class="zw-p-title">${p.hanja} (${p.name})</span>
                    <span class="zw-p-ji">${p.ji_hanja} (${p.ji})</span>
                </div>
                <div class="zw-p-stars">${starsHtml}</div>
                ${sihuaHtml ? `<div class="zw-p-sihua">${sihuaHtml}</div>` : ""}
                <div class="zw-p-desc">${p.desc}</div>
            `;

            grid.appendChild(card);
        });
    }

    // ==========================================================================
    // [2030 바이럴 킬러] 천명 페르소나 스펙 카드 & 현실 팩폭관 렌더링
    // ==========================================================================
    const JIJI_EMOJI = {
        "자": "🐭", "축": "🐂", "인": "🐯", "묘": "🐰", "진": "🐉", "사": "🐍",
        "오": "🐎", "미": "🐑", "신": "🐵", "유": "🐓", "술": "🐕", "해": "🐗"
    };

    function renderMzSpecCard(saju, mzInsight) {
        if (!saju || !mzInsight) return;
        const p = mzInsight.persona || {};
        const raw = saju.raw || {};
        const dayJi = raw.day ? raw.day[1] : "오";
        const emoji = JIJI_EMOJI[dayJi] || "✨";

        safeSetText("mz-character-icon", emoji);
        safeSetText("mz-pillar-tag", `${raw.day || '사주'} (${saju.day_gan || ''} 일간)`);
        safeSetText("mz-character-name", p.title || "천명의 전략가");

        const tagsContainer = document.getElementById("mz-hashtags");
        if (tagsContainer && p.tags) {
            tagsContainer.innerHTML = p.tags.map(t => `<span class="mz-tag">${t}</span>`).join("");
        }

        safeSetText("mz-punchline-text", `"${p.punchline || '내 사주의 팩폭을 직시하라.'}"`);

        // 신강/신약 파워 게이지
        if (saju.strength) {
            const st = saju.strength;
            safeSetText("mz-strength-type", `${st.type} (${st.total_score}점)`);
            const bar = document.getElementById("mz-strength-bar");
            if (bar) bar.style.width = `${Math.min(100, Math.max(10, st.total_score))}%`;
            
            const deukryeongStr = st.deukryeong && st.deukryeong.achieved ? "득령(得令) 35점 통과" : "실령(失令)";
            const deukjiStr = st.deukji && st.deukji.achieved ? "득지(得地) 확보" : "실지(失地)";
            safeSetText("mz-strength-sub", `${deukryeongStr} · ${deukjiStr}`);
        }

        // 조후/억부 용신
        if (saju.yongsin) {
            const ys = saju.yongsin;
            safeSetText("mz-yongsin-name", `${ys.main ? ys.main.toUpperCase() : ''} (${ys.title || '천기처방'})`);
            const presc = ys.prescription || {};
            const luckyContainer = document.getElementById("mz-lucky-tags");
            if (luckyContainer) {
                luckyContainer.innerHTML = `
                    <span class="lucky-chip">🎨 ${presc.color || '행운색'}</span>
                    <span class="lucky-chip">🧭 ${presc.direction || '행운방위'}</span>
                    <span class="lucky-chip">🔢 행운수 ${presc.numbers ? presc.numbers.join(", ") : '7'}</span>
                `;
            }
            safeSetText("mz-yongsin-sub", ys.why || "사주의 균형을 잡는 구원의 오행");
        }

        // 대운 황금기
        if (saju.daeun) {
            const daeun = saju.daeun;
            safeSetText("mz-golden-age", daeun.golden_age_str || "인생 황금기");
            safeSetText("mz-golden-pillar", `간지: ${daeun.golden_pillar || ''}`);
            safeSetText("mz-golden-desc", "천기 용신이 쏟아지는 전성기");
            safeSetText("mz-daeun-direction", `${daeun.direction_name || '순행'} · ${daeun.daeun_number || 4}세 주기`);
        }

        // SNS 공유 버튼 바인딩
        const btnInsta = document.getElementById("btn-share-instagram");
        const btnKakao = document.getElementById("btn-share-kakao");

        const copyShareText = () => {
            const shareText = mzInsight.viral_share_text || "2030 천명 스펙 카드";
            if (navigator.clipboard && navigator.clipboard.writeText) {
                navigator.clipboard.writeText(shareText).then(() => {
                    showToast("📸 [2030 천명 스펙 카드] 클립보드에 복사 완료! 인스타 스토리/카톡에 붙여넣으세요!");
                }).catch(() => {
                    prompt("아래 텍스트를 복사하여 공유하세요:", shareText);
                });
            } else {
                prompt("아래 텍스트를 복사하여 공유하세요:", shareText);
            }
        };

        if (btnInsta) btnInsta.onclick = copyShareText;
        if (btnKakao) btnKakao.onclick = copyShareText;
    }

    // [2030 현실 팩폭관] 렌더링
    function renderMzRealityLab(mzInsight) {
        if (!mzInsight) return;
        const c = mzInsight.career;
        const a = mzInsight.attachment;
        const w = mzInsight.wealth;

        if (c) {
            safeSetText("mz-burnout-badge", `${c.burnout_status || '주의'} (${c.burnout_score || 50}%)`);
            const bBar = document.getElementById("mz-burnout-bar");
            if (bBar) bBar.style.width = `${Math.min(100, Math.max(10, c.burnout_score || 50))}%`;
            safeSetText("mz-burnout-msg", `"${c.burnout_msg || ''}"`);
            safeSetText("mz-turnover-months", c.turnover_months ? c.turnover_months.join(" / ") : "양력 11~1월");
        }

        if (a) {
            safeSetText("mz-attach-badge", a.badge || "애착 유형");
            safeSetText("mz-attach-desc", a.desc || "");
            safeSetText("mz-attach-advice", a.flirting_advice || "");
        }

        if (w) {
            safeSetText("mz-wealth-badge", w.style ? w.style.split(' ')[0] : "재테크 스타일");
            safeSetText("mz-wealth-desc", w.desc || "");
            safeSetText("mz-wealth-tip", w.tip || "");
        }
    }

    // ==========================================================================
    // [2030 혁신 뷰] 도인의 웹툰 시네마틱 옴니버스 리포트 렌더링 (Iris & Cipher)
    // ==========================================================================
    function renderWebtoonReport(saju, spiritVision, lanternFortune, destinyPartners, destinyPlace, cautionCalendar, mzInsight) {
        if (!saju) return;

        // [컷 1] 개안과 운명의 본질
        try {
            const p = saju.pillars;
            const personaTitle = mzInsight && mzInsight.persona ? ` | ${mzInsight.persona.title}` : "";
            const dayPillarName = `${p.day.gan}${p.day.ji} (${p.day.gan_oheng}${p.day.ji_oheng})${personaTitle}`;
            safeSetText("wt-day-pillar-name", dayPillarName);
            if (spiritVision) {
                safeSetText("wt-spirit-name", spiritVision.spirit_name || "청룡 개척령");
                if (spiritVision.obanggi) {
                    safeSetText("wt-obanggi-name", `${spiritVision.obanggi.color}기 (${spiritVision.obanggi.oracle || '안정'})`);
                }
                if (spiritVision.shamanic_speech) {
                    const cleanSpeech = spiritVision.shamanic_speech.replace(/[#*`]/g, '').trim();
                    const snippet = cleanSpeech.length > 140 ? cleanSpeech.slice(0, 140) + "..." : cleanSpeech;
                    safeSetText("wt-speech-1", `"${snippet}"`);
                }
            }
        } catch (e) {
            console.error("wt cut1 error", e);
        }

        // [컷 2] 천명루의 등불 (재물 곳간 / 인연 / 건강)
        try {
            if (lanternFortune && lanternFortune.metrics) {
                const m = lanternFortune.metrics;
                const container = document.getElementById("wt-lantern-container");
                if (container) {
                    container.innerHTML = `
                        <div class="lantern-grid">
                            <div class="lantern-item">
                                <div class="lantern-icon-box" style="${m.wealth && m.wealth.level === 3 ? 'filter: drop-shadow(0 0 16px rgba(255, 215, 0, 0.9));' : ''}">🏮</div>
                                <div class="lantern-info">
                                    <span class="l-label">재물곳간 기운</span>
                                    <strong class="l-status">${m.wealth ? m.wealth.title : '환하게 켜짐'} (${m.wealth ? m.wealth.level : 3}단계)</strong>
                                    <p class="l-desc">${m.wealth ? m.wealth.desc : '금전의 혈맥이 열려 곳간에 재물이 차곡차곡 쌓일 길운입니다.'}</p>
                                </div>
                            </div>
                            <div class="lantern-item">
                                <div class="lantern-icon-box" style="${m.love && m.love.level === 3 ? 'filter: drop-shadow(0 0 16px rgba(255, 215, 0, 0.9));' : ''}">🏮</div>
                                <div class="lantern-info">
                                    <span class="l-label">인연/애정 기운</span>
                                    <strong class="l-status">${m.love ? m.love.title : '은은한 불빛'} (${m.love ? m.love.level : 2}단계)</strong>
                                    <p class="l-desc">${m.love ? m.love.desc : '귀인의 기운이 다가오고 있으나 조급함을 버려야 인연이 맺어집니다.'}</p>
                                </div>
                            </div>
                            <div class="lantern-item">
                                <div class="lantern-icon-box" style="${m.health && m.health.level === 1 ? 'filter: grayscale(60%);' : ''}">🏮</div>
                                <div class="lantern-info">
                                    <span class="l-label">기혈/신체 기운</span>
                                    <strong class="l-status">${m.health ? m.health.title : '주의'} (${m.health ? m.health.level : 1}단계)</strong>
                                    <p class="l-desc">${m.health ? m.health.desc : '신체 통증과 피로가 누적되었으니 기혈 순환과 휴식이 절실합니다.'}</p>
                                </div>
                            </div>
                        </div>
                    `;
                }
                if (m.wealth) {
                    safeSetText("wt-speech-2", `"천명루 처마 밑에 걸린 세 개의 청사초롱을 보아라. 그대의 곳간 등불은 [${m.wealth.title}] 상태이나, 기혈과 건강 등불을 세심히 보살펴야 큰 복을 온전히 담아낼 수 있느니라."`);
                }
            }
        } catch (e) {
            console.error("wt cut2 error", e);
        }

        // [컷 3] 운명의 3대 인연 5대 스펙 카드덱
        try {
            if (destinyPartners && Array.isArray(destinyPartners)) {
                const partnerContainer = document.getElementById("wt-partner-container");
                if (partnerContainer) {
                    partnerContainer.innerHTML = destinyPartners.map((p, idx) => `
                        <div class="partner-spec-card ${p.type === 'nemesis' ? 'is-nemesis' : ''}" id="wt-partner-card-${idx}">
                            <div class="p-card-top">
                                <span class="p-badge">${p.badge}</span>
                                <span class="p-score-tag">궁합 지수: ${p.chemistry_score}점</span>
                            </div>
                            <h4 class="p-title-name">${p.rank_title}</h4>
                            <div class="p-specs-grid">
                                <div class="p-spec-item">
                                    <span class="p-spec-label">이름 초성</span>
                                    <strong class="p-spec-val initial-gold">${p.initial}</strong>
                                </div>
                                <div class="p-spec-item">
                                    <span class="p-spec-label">이상적 키</span>
                                    <strong class="p-spec-val">${p.height}</strong>
                                </div>
                                <div class="p-spec-item">
                                    <span class="p-spec-label">유망 직업군</span>
                                    <strong class="p-spec-val">${p.job}</strong>
                                </div>
                                <div class="p-spec-item">
                                    <span class="p-spec-label">띠 궁합</span>
                                    <strong class="p-spec-val">${p.zodiac}</strong>
                                </div>
                            </div>
                            <div class="p-desc-box" style="margin-bottom:8px;">
                                <strong style="color:var(--gold-light);">외모 및 인상:</strong> ${p.trait}
                            </div>
                            <div class="p-desc-box" style="border-left: 3px solid ${p.type === 'nemesis' ? '#ff4d4f' : '#ffd700'};">
                                <strong style="color:${p.type === 'nemesis' ? '#ffa39e' : '#ffd700'};">도인의 비책:</strong> ${formatMarkdown(p.why_destiny)}
                            </div>
                        </div>
                    `).join("");
                }

                // 바둑알 탭 버튼 인터랙션
                const wtBadukChips = document.querySelectorAll(".wt-baduk-bar .baduk-chip");
                wtBadukChips.forEach(chip => {
                    chip.onclick = () => {
                        wtBadukChips.forEach(c => c.classList.remove("active"));
                        chip.classList.add("active");
                        const targetIdx = chip.dataset.target;
                        const targetCard = document.getElementById(`wt-partner-card-${targetIdx}`);
                        if (targetCard) {
                            targetCard.scrollIntoView({ behavior: "smooth", block: "nearest" });
                            targetCard.style.outline = "2px solid #ffd700";
                            setTimeout(() => { if (targetCard) targetCard.style.outline = "none"; }, 1500);
                        }
                    };
                });
                const primeInitial = destinyPartners[0] ? destinyPartners[0].initial : "ㄱ, ㅂ";
                const dangerInitial = destinyPartners[2] ? destinyPartners[2].initial : "ㅅ, ㅈ";
                safeSetText("wt-speech-3", `"바둑알에 새겨진 세 인연을 똑똑히 보아라... 전생 배필은 [${primeInitial}] 초성의 인연이요, 반면 [${dangerInitial}] 초성의 사람은 그대의 곳간을 흔들 위험이 있으니 깊이 분별하거라."`);
            }
        } catch (e) {
            console.error("wt cut3 error", e);
        }

        // [컷 4] 만남의 공간과 귀인의 방위
        try {
            if (destinyPlace) {
                const placeContainer = document.getElementById("wt-place-container");
                if (placeContainer) {
                    placeContainer.innerHTML = `
                        <div class="place-coords-box">
                            <div class="calligraphy-seal-box">
                                <div class="hanja-seal">${destinyPlace.direction_hanja || "東"}</div>
                                <span class="seal-direction-name">${destinyPlace.direction}쪽 (${(destinyPlace.direction_eng || "").toUpperCase()})</span>
                            </div>
                            <div class="place-details-info">
                                <div class="coord-item">
                                    <span class="coord-label">📍 유리한 거리:</span>
                                    <strong class="coord-val">${destinyPlace.distance || "약 15km 내외"}</strong>
                                </div>
                                <div class="coord-item">
                                    <span class="coord-label">🏛️ 조우 성지 씬:</span>
                                    <strong class="coord-val">${destinyPlace.primary_scene || "조용한 원목 카페 창가"}</strong>
                                </div>
                                <div class="coord-guide-box">
                                    <p class="place-oracle-p">${destinyPlace.oracle_guide || "이 방위는 그대의 부족한 오행을 채워 귀인과의 조우를 성사시키는 천기의 길목입니다."}</p>
                                </div>
                            </div>
                        </div>
                    `;
                }
                safeSetText("wt-speech-4", `"인연과 재물은 가만히 앉아 기다린다고 찾아오지 않는다. 그대에게 가장 길한 방위는 [${destinyPlace.direction}쪽]... ${destinyPlace.primary_scene} 주변으로 발걸음을 옮겨 귀인의 주파수를 맞이하라."`);
            }
        } catch (e) {
            console.error("wt cut4 error", e);
        }

        // [컷 5] 천명 거울과 비책 (살풀이 & 황금 부적)
        try {
            if (cautionCalendar) {
                const salpuriContainer = document.getElementById("wt-salpuri-container");
                if (salpuriContainer) {
                    let schedHtml = "";
                    if (cautionCalendar.schedule && cautionCalendar.schedule.length > 0) {
                        schedHtml = `
                            <div class="caution-schedule-grid" style="margin-top:16px;">
                                <div class="caution-sched-header">
                                    <h4>📅 올 한 해 절대 피해야 할 3대 위험일</h4>
                                    <span class="sched-tag">※ 계약·이직·언쟁 금지</span>
                                </div>
                                <div class="caution-cards-row">
                                    ${cautionCalendar.schedule.map(item => `
                                        <div class="caution-card-item">
                                            <div class="c-seal-stamp">🚨 殺</div>
                                            <div class="c-card-month">${item.month}월 경계령</div>
                                            <div class="c-card-days">위험일: <strong>${item.days.map(d => `${d}일`).join(", ")}</strong></div>
                                            <p class="c-card-reason">${item.reason}</p>
                                        </div>
                                    `).join("")}
                                </div>
                            </div>
                        `;
                    }
                    salpuriContainer.innerHTML = `
                        <div class="salpuri-dday-banner">
                            <div class="dday-badge">⏳ 흉살 소멸 살풀이 골든타임</div>
                            <div class="dday-timer-text">
                                백호·원진 액운 소멸 유효 기간: <strong class="red-glow">D-7일</strong> 남음
                            </div>
                            <p class="dday-sub">이 시기 안에 살풀이 개운 비책을 실천하지 않으면 칼과 쇠, 구설수의 파동이 삶을 덮칠 수 있습니다.</p>
                        </div>
                        ${schedHtml}
                        <div class="amulet-banner" style="margin-top:20px;">
                            <div class="amulet-badge">🎴 현허도인의 맞춤 천기 황금 부적</div>
                            <div class="amulet-content-row">
                                <div class="amulet-visual">
                                    <div class="amulet-paper">
                                        <div class="amulet-red-box">
                                            <span class="amulet-seal-top">敕令</span>
                                            <span class="amulet-center-text">萬事如意符</span>
                                            <span class="amulet-seal-bot">急急如律令</span>
                                        </div>
                                    </div>
                                </div>
                                <div class="amulet-text-info">
                                    <h4 class="amulet-title">청룡벽사 만사여의부</h4>
                                    <p class="amulet-desc">흉살을 물리치고 막힌 기운을 뚫어 만사가 뜻대로 풀리게 하는 황금 수호 비책입니다.</p>
                                    <button type="button" class="share-amulet-btn wt-btn-open-amulet">📲 부적 다운로드 및 카톡/인스타 저장</button>
                                </div>
                            </div>
                        </div>
                    `;

                    const wtAmuletBtn = salpuriContainer.querySelector(".wt-btn-open-amulet");
                    if (wtAmuletBtn && downloadAmuletBtn) {
                        wtAmuletBtn.addEventListener("click", () => {
                            downloadAmuletBtn.click();
                        });
                    }
                }
                safeSetText("wt-speech-5", `"골든타임 D-7일! 거울에 비친 흉살의 그림자를 씻어내고, 황금 부적을 폰에 저장하거나 품에 간직하라. 불운이 비껴가고 귀인의 빛이 비출 것이다."`);
            }
        } catch (e) {
            console.error("wt cut5 error", e);
        }
    }

    // [청월당 킬러 포맷 1] 청사초롱 5색 기운 등불 진단 렌더링
    function renderLanternFortune(lantern) {
        if (!lantern || !lantern.metrics) return;
        const m = lantern.metrics;

        const setLanternItem = (type, data) => {
            const statusEl = document.getElementById(`lantern-${type}-status`);
            const descEl = document.getElementById(`lantern-${type}-desc`);
            const iconEl = document.getElementById(`lantern-${type}-icon`);
            if (statusEl) statusEl.textContent = `${data.title} (${data.level}단계)`;
            if (descEl) descEl.textContent = data.desc;
            if (iconEl) {
                if (data.level === 3) {
                    iconEl.style.filter = "drop-shadow(0 0 16px rgba(255, 215, 0, 0.9))";
                    iconEl.textContent = "🏮✨";
                } else if (data.level === 2) {
                    iconEl.style.filter = "drop-shadow(0 0 8px rgba(255, 165, 0, 0.6))";
                    iconEl.textContent = "🏮";
                } else {
                    iconEl.style.filter = "grayscale(60%) opacity(0.7)";
                    iconEl.textContent = "🏮💨";
                }
            }
        };

        if (m.wealth) setLanternItem("wealth", m.wealth);
        if (m.love) setLanternItem("love", m.love);
        if (m.health) setLanternItem("health", m.health);
    }

    // [청월당 킬러 포맷 2] 살풀이 골든타임 D-Day & 월별 주의일 달력 렌더링
    function renderCautionCalendar(caution) {
        if (!caution) return;
        const container = document.getElementById("caution-cards-container");
        if (!container) return;

        if (caution.schedule && caution.schedule.length > 0) {
            container.innerHTML = caution.schedule.map(item => `
                <div class="caution-card-item">
                    <div class="c-seal-stamp">🚨 殺</div>
                    <div class="c-card-month">${item.month}월 경계령</div>
                    <div class="c-card-days">위험일: <strong>${item.days.map(d => `${d}일`).join(", ")}</strong></div>
                    <p class="c-card-reason">${item.reason}</p>
                </div>
            `).join("");
        }
    }

    // [청월당 킬러 포맷 3] 운명의 3대 인연 5대 스펙 카드덱 렌더링
    function renderDestinyPartners(partners) {
        if (!partners || !Array.isArray(partners)) return;
        const container = document.getElementById("partner-cards-container");
        if (!container) return;

        container.innerHTML = partners.map((p, idx) => `
            <div class="partner-spec-card ${p.type === 'nemesis' ? 'is-nemesis' : ''}" id="partner-card-${idx}">
                <div class="p-card-top">
                    <span class="p-badge">${p.badge}</span>
                    <span class="p-score-tag">궁합 지수: ${p.chemistry_score}점</span>
                </div>
                <h4 class="p-title-name">${p.rank_title}</h4>
                <div class="p-specs-grid">
                    <div class="p-spec-item">
                        <span class="p-spec-label">이름 초성 (성명학)</span>
                        <strong class="p-spec-val initial-gold">${p.initial}</strong>
                    </div>
                    <div class="p-spec-item">
                        <span class="p-spec-label">이상적인 키</span>
                        <strong class="p-spec-val">${p.height}</strong>
                    </div>
                    <div class="p-spec-item">
                        <span class="p-spec-label">유망 직업군</span>
                        <strong class="p-spec-val">${p.job}</strong>
                    </div>
                    <div class="p-spec-item">
                        <span class="p-spec-label">띠 (삼합/원진)</span>
                        <strong class="p-spec-val">${p.zodiac}</strong>
                    </div>
                </div>
                <div class="p-desc-box" style="margin-bottom:8px;">
                    <strong style="color:var(--gold-light);">외모 및 분위기:</strong> ${p.trait}
                </div>
                <div class="p-desc-box" style="margin-bottom:8px;">
                    <strong style="color:var(--gold-light);">조우 타이밍:</strong> ${p.meeting_timing}
                </div>
                <div class="p-desc-box" style="border-left: 3px solid ${p.type === 'nemesis' ? '#ff4d4f' : '#ffd700'};">
                    <strong style="color:${p.type === 'nemesis' ? '#ffa39e' : '#ffd700'};">도인의 직설 비책:</strong> ${formatMarkdown(p.why_destiny)}
                </div>
            </div>
        `).join("");

        // 바둑알 탭 인터랙션
        const chips = document.querySelectorAll(".baduk-chip");
        chips.forEach(chip => {
            chip.onclick = () => {
                chips.forEach(c => c.classList.remove("active"));
                chip.classList.add("active");
                const targetIdx = chip.dataset.target;
                const targetCard = document.getElementById(`partner-card-${targetIdx}`);
                if (targetCard) {
                    targetCard.scrollIntoView({ behavior: "smooth", block: "nearest" });
                    targetCard.style.outline = "2px solid #ffd700";
                    setTimeout(() => { if (targetCard) targetCard.style.outline = "none"; }, 1500);
                }
            };
        });
    }

    // [청월당 킬러 포맷 4] 동서남북 붓글씨 3차원 공간 좌표 렌더링
    function renderDestinyPlace(place) {
        if (!place) return;
        safeSetText("place-hanja-seal", place.direction_hanja || "東");
        safeSetText("place-dir-name", `${place.direction}쪽 (${(place.direction_eng || "").toUpperCase()})`);
        safeSetText("place-distance-text", place.distance || "-");
        safeSetText("place-scene-text", place.primary_scene || "-");
        safeSetHtml("place-oracle-guide", formatMarkdown(place.oracle_guide || ""));
    }

    function renderPillarCell(prefix, pillar) {
        document.getElementById(`${prefix}-gan`).innerHTML = `<span class="oheng-color-${pillar.gan_oheng[0]}">${pillar.gan}</span>`;
        document.getElementById(`${prefix}-ji`).innerHTML = `<span class="oheng-color-${pillar.ji_oheng[0]}">${pillar.ji}</span>`;
        const ganSip = document.getElementById(`${prefix}-gan-sip`);
        const jiSip = document.getElementById(`${prefix}-ji-sip`);
        const unsung = document.getElementById(`${prefix}-unsung`);
        const jijanggan = document.getElementById(`${prefix}-jijanggan`);
        if (ganSip) ganSip.textContent = pillar.gan_sipseong;
        if (jiSip) jiSip.textContent = pillar.ji_sipseong;
        if (unsung) unsung.textContent = pillar.unsung;
        if (jijanggan) jijanggan.textContent = pillar.jijanggan.join("·");
    }

    function renderRadarChart(sixSenses) {
        const svg = document.getElementById("radar-svg");
        const listElem = document.getElementById("six-senses-list");
        svg.innerHTML = "";
        listElem.innerHTML = "";

        const cx = 160, cy = 160, maxR = 100, total = 6;
        for (let level = 1; level <= 5; level++) {
            const r = (maxR / 5) * level;
            let points = [];
            for (let i = 0; i < total; i++) {
                const angle = (2 * Math.PI * i / total) - (Math.PI / 2);
                points.push(`${cx + r * Math.cos(angle)},${cy + r * Math.sin(angle)}`);
            }
            const polygon = document.createElementNS("http://www.w3.org/2000/svg", "polygon");
            polygon.setAttribute("points", points.join(" "));
            polygon.setAttribute("fill", level === 5 ? "rgba(212, 175, 55, 0.05)" : "none");
            polygon.setAttribute("stroke", "rgba(212, 175, 55, 0.2)");
            polygon.setAttribute("stroke-width", "1");
            svg.appendChild(polygon);
        }

        let dataPoints = [];
        sixSenses.forEach((item, i) => {
            const angle = (2 * Math.PI * i / total) - (Math.PI / 2);
            const line = document.createElementNS("http://www.w3.org/2000/svg", "line");
            line.setAttribute("x1", cx); line.setAttribute("y1", cy);
            line.setAttribute("x2", cx + maxR * Math.cos(angle));
            line.setAttribute("y2", cy + maxR * Math.sin(angle));
            line.setAttribute("stroke", "rgba(212, 175, 55, 0.2)");
            svg.appendChild(line);

            const text = document.createElementNS("http://www.w3.org/2000/svg", "text");
            text.setAttribute("x", cx + (maxR + 25) * Math.cos(angle));
            text.setAttribute("y", cy + (maxR + 25) * Math.sin(angle) + 4);
            text.setAttribute("fill", "#b5b0a3");
            text.setAttribute("font-size", "11");
            text.setAttribute("font-family", "var(--font-serif)");
            text.setAttribute("text-anchor", "middle");
            text.textContent = item.label;
            svg.appendChild(text);

            const scoreR = (maxR / 5) * item.score;
            dataPoints.push(`${cx + scoreR * Math.cos(angle)},${cy + scoreR * Math.sin(angle)}`);

            const stars = "★".repeat(item.score) + "☆".repeat(5 - item.score);
            const div = document.createElement("div");
            div.className = "sense-item";
            div.innerHTML = `<span class="sense-label">${item.label} (${item.hanja})</span><span class="sense-stars">${stars}</span>`;
            listElem.appendChild(div);
        });

        const dataPolygon = document.createElementNS("http://www.w3.org/2000/svg", "polygon");
        dataPolygon.setAttribute("points", dataPoints.join(" "));
        dataPolygon.setAttribute("fill", "rgba(212, 175, 55, 0.35)");
        dataPolygon.setAttribute("stroke", "#d4af37");
        dataPolygon.setAttribute("stroke-width", "2");
        svg.appendChild(dataPolygon);
    }

    function renderGates(gates) {
        const container = document.getElementById("gates-list");
        container.innerHTML = gates.map(gate => `
            <div class="gate-card ${gate.opened ? "opened" : ""}">
                <div class="gate-header">
                    <span class="gate-name">${gate.name}</span>
                    <span class="gate-status">${gate.opened ? "열림 (開)" : "닫힘 (閉)"}</span>
                </div>
                <p class="gate-desc">${gate.desc}</p>
            </div>
        `).join("");
    }

    // 11개 챕터 렌더링 (잠금/해제 인터랙션)
    function renderChapters(categoryFilter) {
        const container = document.getElementById("chapters-container");
        container.innerHTML = "";

        const filtered = categoryFilter === "all" 
            ? chaptersData 
            : chaptersData.filter(ch => ch.category === categoryFilter);

        filtered.forEach((ch, idx) => {
            const item = document.createElement("div");
            item.className = "chapter-item" + (idx === 0 ? " open" : "");
            
            // 잠겨있는 챕터인 경우
            if (ch.is_locked) {
                item.innerHTML = `
                    <div class="chapter-header">
                        <div class="ch-title-group">
                            <span class="ch-hanja">🔒</span>
                            <div><div class="ch-title">${ch.title} <span style="font-size:0.78rem; color:#e74c3c;">[VIP 잠금]</span></div></div>
                        </div>
                        <div style="display:flex; align-items:center; gap:8px;">
                            <span class="ch-category">${ch.category}</span>
                            <span class="ch-arrow">▼</span>
                        </div>
                    </div>
                    <div class="chapter-body">
                        <div class="grandma-voice-box locked-blur">${ch.locked_preview}</div>
                        <div class="lock-cta-box">
                            <p style="color:var(--gold-light); font-weight:700; margin-bottom:6px;">🔒 이 챕터는 VIP 전체 풀이에서 확인하실 수 있습니다.</p>
                            <p style="font-size:0.85rem; color:var(--text-muted); margin-bottom:10px;">재물 창고의 크기, 이직 타이밍, 대운의 황금기, 운명의 갈림길 비책</p>
                            <button type="button" class="lock-cta-btn" onclick="document.getElementById('open-paywall-btn').click()">👑 19,800원으로 전체 잠금 해제하기</button>
                        </div>
                    </div>
                `;
            } else {
                item.innerHTML = `
                    <div class="chapter-header">
                        <div class="ch-title-group">
                            <span class="ch-hanja">${ch.hanja}</span>
                            <div><div class="ch-title">${ch.title}</div></div>
                        </div>
                        <div style="display:flex; align-items:center; gap:8px;">
                            <span class="ch-category">${ch.category}</span>
                            <span class="ch-arrow">▼</span>
                        </div>
                    </div>
                    <div class="chapter-body">
                        <div class="grandma-voice-box">${formatMarkdown(ch.desc)}</div>
                        <div class="fate-contrast-grid">
                            <div class="fate-card good-fate">
                                <span class="fate-tag-good">✨ 잘 풀렸을 때 (천운의 모습)</span>
                                <p>${formatMarkdown(ch.good)}</p>
                            </div>
                            <div class="fate-card bad-fate">
                                <span class="fate-tag-bad">⚡ 안 풀렸을 때 (악운의 모습)</span>
                                <p>${formatMarkdown(ch.bad)}</p>
                            </div>
                        </div>
                        <div class="advice-scroll">
                            <div class="advice-title">📜 현허도인의 개운 비책</div>
                            <div class="advice-content">${formatMarkdown(ch.advice)}</div>
                        </div>
                    </div>
                `;
            }

            const header = item.querySelector(".chapter-header");
            header.addEventListener("click", () => {
                item.classList.toggle("open");
            });

            container.appendChild(item);
        });
    }

    // 카테고리 탭
    document.querySelectorAll(".cat-btn").forEach(btn => {
        btn.addEventListener("click", () => {
            document.querySelectorAll(".cat-btn").forEach(b => b.classList.remove("active"));
            btn.classList.add("active");
            renderChapters(btn.dataset.cat);
        });
    });

    // VIP 페이월 모달 오픈
    openPaywallBtn.addEventListener("click", () => {
        paywallModal.classList.remove("hidden");
    });

    modalCloseBtn.addEventListener("click", () => {
        paywallModal.classList.add("hidden");
    });

    // VIP 결제 시뮬레이션
    simulatePayBtn.addEventListener("click", async () => {
        try {
            const resp = await fetch("/api/unlock", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ order_id: `ORDER-${Date.now()}` })
            });
            const data = await resp.json();
            if (data.status === "success") {
                isVipUnlocked = true;
                paywallModal.classList.add("hidden");
                alert("🎉 [결제 완료] VIP 평생 열람 권한이 성공적으로 활성화되었습니다! 52장 전체 리포트가 모두 잠금 해제되었습니다.");
                
                // 다시 렌더링
                chaptersData.forEach(ch => ch.is_locked = false);
                renderChapters("all");
                document.getElementById("vip-paywall-banner").style.display = "none";
            }
        } catch (e) {
            alert("결제 처리 중 오류 발생: " + e.message);
        }
    });

    // 부적 캔버스 생성 및 모달
    downloadAmuletBtn.addEventListener("click", () => {
        if (!cachedGlobal) return;
        drawAmuletCanvas(cachedGlobal.amulet.name, currentUserName);
        amuletModal.classList.remove("hidden");
    });

    amuletCloseBtn.addEventListener("click", () => {
        amuletModal.classList.add("hidden");
    });

    function drawAmuletCanvas(amuletTitle, name) {
        const ctx = amuletCanvas.getContext("2d");
        const w = amuletCanvas.width;
        const h = amuletCanvas.height;

        // 전통 황금 한지 배경
        const grad = ctx.createLinearGradient(0, 0, w, h);
        grad.addColorStop(0, "#e8c973");
        grad.addColorStop(0.5, "#d6ad45");
        grad.addColorStop(1, "#c59a30");
        ctx.fillStyle = grad;
        ctx.fillRect(0, 0, w, h);

        // 옻칠 테두리
        ctx.strokeStyle = "#4a350d";
        ctx.lineWidth = 12;
        ctx.strokeRect(10, 10, w - 20, h - 20);

        ctx.strokeStyle = "#8e6c1e";
        ctx.lineWidth = 2;
        ctx.strokeRect(18, 18, w - 36, h - 36);

        // 주사 붉은 상단 글씨 (맑은 고딕 적용)
        ctx.fillStyle = "#b83b3b";
        ctx.font = "bold 22px 'Malgun Gothic', '맑은 고딕', sans-serif";
        ctx.textAlign = "center";
        ctx.fillText("현허도인 천기 황금부적", w / 2, 60);

        ctx.font = "bold 15px 'Malgun Gothic', '맑은 고딕', sans-serif";
        ctx.fillStyle = "#5c4015";
        ctx.fillText(`[${name}] 귀하의 액운 소멸 & 천운 개운`, w / 2, 90);

        // 중앙 붉은 족자 박스
        ctx.fillStyle = "rgba(184, 59, 59, 0.08)";
        ctx.fillRect(50, 120, w - 100, 400);
        ctx.strokeStyle = "#b83b3b";
        ctx.lineWidth = 3;
        ctx.strokeRect(50, 120, w - 100, 400);

        // 부적 주사 글씨
        ctx.fillStyle = "#b83b3b";
        ctx.font = "bold 38px 'Malgun Gothic', '맑은 고딕', sans-serif";
        ctx.fillText("敕 令", w / 2, 180);

        // 세로 부적 이름
        ctx.font = "bold 30px 'Malgun Gothic', '맑은 고딕', sans-serif";
        const chars = amuletTitle.slice(0, 7);
        let startY = 240;
        for (let i = 0; i < chars.length; i++) {
            ctx.fillText(chars[i], w / 2, startY + (i * 38));
        }

        ctx.font = "bold 24px 'Malgun Gothic', '맑은 고딕', sans-serif";
        ctx.fillText("急急如律令", w / 2, 490);

        // 하단 인장
        ctx.font = "bold 13px 'Malgun Gothic', '맑은 고딕', sans-serif";
        ctx.fillStyle = "#5c4015";
        ctx.fillText("동양 정통 명리학 & 현허도인 천기 신점", w / 2, 555);
        ctx.fillText("© 天命明鏡 (천명명경)", w / 2, 575);
    }

    saveCanvasBtn.addEventListener("click", () => {
        const link = document.createElement("a");
        link.download = `현허도인_천기부적_${currentUserName}.png`;
        link.href = amuletCanvas.toDataURL("image/png");
        link.click();
    });

    // ==========================================================================
    // 2대 뷰 모드 스위처 & 버튼 전수 바인딩 (Sentinel & Cipher 안전망 구축)
    // ==========================================================================
    const btnViewWebtoon = document.getElementById("btn-view-webtoon");
    const btnViewDetailed = document.getElementById("btn-view-detailed");
    const resultWebtoonMode = document.getElementById("result-webtoon-mode");
    const resultDetailedMode = document.getElementById("result-detailed-mode");
    const btnSwitchToDetailed = document.getElementById("btn-switch-to-detailed");

    function switchResultView(mode) {
        if (mode === "webtoon") {
            if (btnViewWebtoon) btnViewWebtoon.classList.add("active");
            if (btnViewDetailed) btnViewDetailed.classList.remove("active");
            if (resultWebtoonMode) resultWebtoonMode.classList.remove("hidden");
            if (resultDetailedMode) resultDetailedMode.classList.add("hidden");
        } else {
            if (btnViewWebtoon) btnViewWebtoon.classList.remove("active");
            if (btnViewDetailed) btnViewDetailed.classList.add("active");
            if (resultWebtoonMode) resultWebtoonMode.classList.add("hidden");
            if (resultDetailedMode) resultDetailedMode.classList.remove("hidden");
        }
    }

    if (btnViewWebtoon) {
        btnViewWebtoon.addEventListener("click", () => switchResultView("webtoon"));
    }
    if (btnViewDetailed) {
        btnViewDetailed.addEventListener("click", () => switchResultView("detailed"));
    }
    if (btnSwitchToDetailed) {
        btnSwitchToDetailed.addEventListener("click", () => {
            switchResultView("detailed");
            if (resultDetailedMode) {
                resultDetailedMode.scrollIntoView({ behavior: "smooth" });
            }
        });
    }

    // 감명 요약 클립보드 복사 공통 함수
    function copySajuSummaryToClipboard(showToastFlag = true) {
        if (!cachedSaju || !cachedSpirit) {
            if (showToastFlag) showToast("감명 데이터가 없습니다.");
            return;
        }
        try {
            const p = cachedSaju.pillars;
            const fourPillars = `${p.year.gan_hanja}${p.year.ji_hanja}년 ${p.month.gan_hanja}${p.month.ji_hanja}월 ${p.day.gan_hanja}${p.day.ji_hanja}일 ${p.hour.gan_hanja}${p.hour.ji_hanja}시`;
            
            let ziweiSummaryLine = "";
            if (cachedZiwei && cachedZiwei.ming_palace) {
                const mStars = cachedZiwei.ming_palace.stars.map(s => s.name).join("·") || "무주성";
                const bureau = cachedZiwei.bureau ? cachedZiwei.bureau.name : "";
                const hwayi = cachedZiwei.sihua && cachedZiwei.sihua.기 ? `${cachedZiwei.sihua.기.palace}(${cachedZiwei.sihua.기.star}化忌)` : "";
                ziweiSummaryLine = `• 자미두수: ${bureau} | 명궁 [${mStars}] | 시련 [${hwayi}]\n`;
            }

            const summaryText = `[天命明鏡 (천명명경) 사주 신점 감명 요약]\n\n` +
                `• 명식: ${fourPillars} (${cachedSaju.day_gan} 일간)\n` +
                ziweiSummaryLine +
                `• 수호신령: ${cachedSpirit.spirit_name}\n` +
                `• 신체 통증 투시: ${cachedSpirit.body_pain}\n` +
                `• 과거 환란 적중: ${cachedSpirit.recent_shock}\n` +
                `• 오방기 신탁: [${cachedSpirit.obanggi.color}] ${cachedSpirit.obanggi.oracle}\n` +
                `• 현허도인 칙명: ${cachedReading && cachedReading.sections && cachedReading.sections[10] ? cachedReading.sections[10].desc.slice(0, 120) : ''}...\n\n` +
                `© 天命明鏡 현허도인 천기 신점`;

            navigator.clipboard.writeText(summaryText).then(() => {
                if (showToastFlag) showToast("📋 감명 요약이 클립보드에 복사되었습니다!");
            }).catch(() => {
                if (showToastFlag) showToast("클립보드 복사에 실패했습니다.");
            });
        } catch (err) {
            if (showToastFlag) showToast("복사 중 오류가 발생했습니다.");
        }
    }

    if (copySummaryBtn) {
        copySummaryBtn.addEventListener("click", () => copySajuSummaryToClipboard(true));
    }

    // 100% 무결점 보장: 상단/하단 모든 인쇄 및 저장 버튼 전수 바인딩
    const allPrintBtns = document.querySelectorAll(".btn-print, #print-result-btn, #bottom-print-btn, #print-btn");
    allPrintBtns.forEach(btn => {
        btn.addEventListener("click", (e) => {
            e.preventDefault();
            showToast("🖨️ 현허도인의 천기 감명서 인쇄 및 저장을 준비합니다...");
            copySajuSummaryToClipboard(false); // 백업 자동 복사
            setTimeout(() => {
                window.print();
            }, 300);
        });
    });

    // 100% 무결점 보장: 상단/하단 모든 다시보기 버튼 전수 바인딩
    const allRestartBtns = document.querySelectorAll(".btn-restart, #restart-btn, #bottom-restart-btn");
    allRestartBtns.forEach(btn => {
        btn.addEventListener("click", (e) => {
            e.preventDefault();
            if (resultSection) resultSection.classList.add("hidden");
            if (inputSection) inputSection.classList.remove("hidden");
            window.scrollTo({ top: 0, behavior: 'smooth' });
            showToast("🔄 새로운 사주를 입력하실 수 있습니다.");
        });
    });

    /* ==========================================================================
       다크사주 100% 흡수: 3대 메인 탭바 & 교차 궁합실 & 1:1 문답 & 출석 스탬프 (Cipher Implementation)
       ========================================================================== */
    
    // 1. 3대 메인 탭 전환 로직 (2030 모던 미니멀 스타일)
    const tabBtnSaju = document.getElementById("tab-btn-saju");
    const tabBtnGunghap = document.getElementById("tab-btn-gunghap");
    const tabBtnQa = document.getElementById("tab-btn-qa");
    const webtoonIntroSection = document.getElementById("webtoon-intro-section");
    const gunghapSection = document.getElementById("gunghap-section");
    const qaSection = document.getElementById("qa-section");

    function switchMainTab(targetTab) {
        [tabBtnSaju, tabBtnGunghap, tabBtnQa].forEach(btn => {
            if (btn) btn.classList.remove("active");
        });

        if (targetTab === "saju") {
            if (tabBtnSaju) tabBtnSaju.classList.add("active");
            if (gunghapSection) gunghapSection.classList.add("hidden");
            if (qaSection) qaSection.classList.add("hidden");
            if (cachedGlobal) {
                resultSection.classList.remove("hidden");
                inputSection.classList.add("hidden");
                if (webtoonIntroSection) webtoonIntroSection.classList.add("hidden");
            } else {
                resultSection.classList.add("hidden");
                if (inputSection.classList.contains("hidden") && webtoonIntroSection && webtoonIntroSection.classList.contains("hidden")) {
                    webtoonIntroSection.classList.remove("hidden");
                }
                window.scrollTo({ top: 0, behavior: "smooth" });
            }
        } else if (targetTab === "gunghap") {
            if (tabBtnGunghap) tabBtnGunghap.classList.add("active");
            if (webtoonIntroSection) webtoonIntroSection.classList.add("hidden");
            inputSection.classList.add("hidden");
            resultSection.classList.add("hidden");
            if (qaSection) qaSection.classList.add("hidden");
            if (gunghapSection) gunghapSection.classList.remove("hidden");
            window.scrollTo({ top: gunghapSection.offsetTop - 80, behavior: "smooth" });
        } else if (targetTab === "qa") {
            if (tabBtnQa) tabBtnQa.classList.add("active");
            if (webtoonIntroSection) webtoonIntroSection.classList.add("hidden");
            inputSection.classList.add("hidden");
            resultSection.classList.add("hidden");
            if (gunghapSection) gunghapSection.classList.add("hidden");
            if (qaSection) qaSection.classList.remove("hidden");
            window.scrollTo({ top: qaSection.offsetTop - 80, behavior: "smooth" });
        }
    }

    if (tabBtnSaju) tabBtnSaju.addEventListener("click", () => switchMainTab("saju"));
    if (tabBtnGunghap) tabBtnGunghap.addEventListener("click", () => switchMainTab("gunghap"));
    if (tabBtnQa) tabBtnQa.addEventListener("click", () => switchMainTab("qa"));

    // 도인의 거울 개안 플래시 트랜지션 함수
    const mirrorFlashEl = document.getElementById("mirror-flash");

    function triggerMirrorTransition(callback) {
        if (mirrorFlashEl) {
            mirrorFlashEl.classList.add("flashing");
            setTimeout(() => {
                if (callback) callback();
                window.scrollTo({ top: 0, behavior: "instant" });
                setTimeout(() => {
                    mirrorFlashEl.classList.remove("flashing");
                }, 300);
            }, 350);
        } else {
            if (callback) callback();
            window.scrollTo({ top: 0, behavior: "smooth" });
        }
    }

    // 웹툰 건너뛰기 퀵 버튼 (Step 1 -> Step 2 즉시 전환)
    const btnSkipWebtoon = document.getElementById("btn-skip-webtoon");
    if (btnSkipWebtoon) {
        btnSkipWebtoon.addEventListener("click", () => {
            if (webtoonIntroSection) webtoonIntroSection.classList.add("hidden");
            if (inputSection) inputSection.classList.remove("hidden");
            window.scrollTo({ top: 0, behavior: "smooth" });
        });
    }

    // 인라인 웹툰 4컷 "거울 터치하고 내 사주 밝히기" 버튼 (Step 1 -> Step 2 시네마틱 개안 전환!)
    const btnEnterSajuFromInlineWebtoon = document.getElementById("btn-enter-saju-from-inline-webtoon");
    if (btnEnterSajuFromInlineWebtoon) {
        btnEnterSajuFromInlineWebtoon.addEventListener("click", () => {
            triggerMirrorTransition(() => {
                if (webtoonIntroSection) webtoonIntroSection.classList.add("hidden");
                if (inputSection) inputSection.classList.remove("hidden");
                showToast("🪞 도인의 천명 거울이 열렸습니다. 그대의 사주를 입력하십시오.");
            });
        });
    }

    // 웹툰 다시보기 버튼 (Step 2 -> Step 1 전환)
    const btnReopenWebtoon = document.getElementById("btn-reopen-webtoon");
    if (btnReopenWebtoon) {
        btnReopenWebtoon.addEventListener("click", () => {
            if (webtoonIntroSection) webtoonIntroSection.classList.remove("hidden");
            if (inputSection) inputSection.classList.add("hidden");
            window.scrollTo({ top: 0, behavior: "smooth" });
        });
    }

    // 2. 2인 사주 교차 궁합실 로직
    let selectedRelation = "dating";
    const relationChips = document.querySelectorAll(".relation-chip");
    relationChips.forEach(chip => {
        chip.addEventListener("click", () => {
            relationChips.forEach(c => c.classList.remove("active"));
            chip.classList.add("active");
            selectedRelation = chip.dataset.relation || "dating";
        });
    });

    // 궁합 성별 미니 칩 선택
    const miniChips = document.querySelectorAll(".mini-chip");
    miniChips.forEach(chip => {
        chip.addEventListener("click", () => {
            const targetId = chip.dataset.target;
            const targetInput = document.getElementById(targetId);
            if (targetInput) {
                targetInput.value = chip.dataset.val;
                chip.parentElement.querySelectorAll(".mini-chip").forEach(c => c.classList.remove("active"));
                chip.classList.add("active");
            }
        });
    });

    const btnSubmitGunghap = document.getElementById("btn-submit-gunghap");
    const gunghapResultCard = document.getElementById("gunghap-result");

    if (btnSubmitGunghap) {
        btnSubmitGunghap.addEventListener("click", async () => {
            const nameA = document.getElementById("gh-name-a")?.value || "본인";
            const yearA = parseInt(document.getElementById("gh-year-a")?.value || "1994");
            const monthA = parseInt(document.getElementById("gh-month-a")?.value || "3");
            const dayA = parseInt(document.getElementById("gh-day-a")?.value || "15");
            const hourA = parseInt(document.getElementById("gh-hour-a")?.value || "18");
            const genderA = document.getElementById("gh-gender-a")?.value || "male";

            const nameB = document.getElementById("gh-name-b")?.value || "상대방";
            const yearB = parseInt(document.getElementById("gh-year-b")?.value || "1995");
            const monthB = parseInt(document.getElementById("gh-month-b")?.value || "5");
            const dayB = parseInt(document.getElementById("gh-day-b")?.value || "20");
            const hourB = parseInt(document.getElementById("gh-hour-b")?.value || "10");
            const genderB = document.getElementById("gh-gender-b")?.value || "female";

            btnSubmitGunghap.disabled = true;
            btnSubmitGunghap.innerHTML = "<span>🔮 두 영혼의 사주와 자미두수 명궁을 교차 분석 중...</span>";

            try {
                const res = await fetch("/api/gunghap", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({
                        relation: selectedRelation,
                        person_a: { name: nameA, year: yearA, month: monthA, day: dayA, hour: hourA, gender: genderA, is_lunar: false },
                        person_b: { name: nameB, year: yearB, month: monthB, day: dayB, hour: hourB, gender: genderB, is_lunar: false }
                    })
                });

                const data = await res.json();
                if (data.status === "success") {
                    const gh = data.gunghap;
                    renderGunghapResult(gh, nameA, nameB);
                } else {
                    showToast("궁합 분석 오류: " + (data.message || "알 수 없는 오류"));
                }
            } catch (err) {
                showToast("서버 통신 실패: " + err.message);
            } finally {
                btnSubmitGunghap.disabled = false;
                btnSubmitGunghap.innerHTML = "<span>💞 두 사람의 천기 궁합 분석하기</span>";
            }
        });
    }

    function renderGunghapResult(gh, nameA, nameB) {
        if (!gunghapResultCard) return;

        const relLabels = {
            unrequited: "💘 짝사랑/고백 궁합",
            dating: "💞 썸/연애 궁합",
            married: "💍 부부/결혼 궁합",
            business: "💼 업무/동업 궁합"
        };

        const badgeEl = document.getElementById("gh-rel-badge");
        if (badgeEl) badgeEl.textContent = relLabels[gh.relation] || "💞 천기 궁합";

        const totalScoreEl = document.getElementById("gh-total-score");
        if (totalScoreEl) totalScoreEl.textContent = gh.total_score;

        const gradeEl = document.getElementById("gh-grade");
        if (gradeEl) gradeEl.textContent = `${gh.grade} (합치도 ${gh.total_score}점)`;

        const gradeDescEl = document.getElementById("gh-grade-desc");
        if (gradeDescEl) gradeDescEl.textContent = `[${nameA}] 님과 [${nameB}] 님의 천간합·지지합·오행 상호보완 분석 결과입니다.`;

        // 지표 바 업데이트
        const setMetric = (barId, valId, score) => {
            const bar = document.getElementById(barId);
            const val = document.getElementById(valId);
            if (bar) bar.style.width = `${Math.min(100, Math.max(10, score))}%`;
            if (val) val.textContent = `${score}%`;
        };

        setMetric("bar-spirit", "val-spirit", gh.details.gan_chemistry.score);
        setMetric("bar-reality", "val-reality", gh.details.ji_chemistry.score);
        setMetric("bar-elem", "val-elem", gh.details.elem_balance.score);
        setMetric("bar-social", "val-social", gh.details.year_chemistry.score);

        // 현허도인의 직설 공수
        const speechEl = document.getElementById("gh-speech-text");
        if (speechEl) speechEl.textContent = gh.relation_reading;

        gunghapResultCard.classList.remove("hidden");
        gunghapResultCard.scrollIntoView({ behavior: "smooth", block: "start" });
        showToast("✨ 두 사람의 천기 교차 궁합이 완성되었습니다!");
    }

    // 3. 1:1 천기 심층 문답소 로직
    let selectedQaMode = "single";
    const qaModeChips = document.querySelectorAll(".qa-mode-chip");
    qaModeChips.forEach(chip => {
        chip.addEventListener("click", () => {
            qaModeChips.forEach(c => c.classList.remove("active"));
            chip.classList.add("active");
            selectedQaMode = chip.dataset.mode || "single";
        });
    });

    // 추천 질문 칩 클릭
    const presetChips = document.querySelectorAll(".preset-chip");
    const qaInputText = document.getElementById("qa-input-text");
    presetChips.forEach(chip => {
        chip.addEventListener("click", () => {
            if (qaInputText) {
                qaInputText.value = chip.textContent.trim();
                qaInputText.focus();
            }
        });
    });

    const qaChatHistory = document.getElementById("qa-chat-history");
    const btnSendQa = document.getElementById("btn-send-qa");
    let qaHistory = [];

    // 다크사주 18종 금기어 블랙리스트
    const TABOO_KEYWORDS = [
        "프롬트", "프롬프트", "prompt", "스키마", "스킴", "schema", "json",
        "배팅", "베팅", "로또", "비트코인", "주식", "슬롯", "승률", "경마", "카지노", "상한가", "하한가", "일확천금"
    ];

    function checkTabooKeyword(text) {
        const lower = text.toLowerCase();
        for (const word of TABOO_KEYWORDS) {
            if (lower.includes(word.toLowerCase())) return word;
        }
        return null;
    }

    function appendChatMessage(sender, text, isWarning = false) {
        if (!qaChatHistory) return null;

        const msgDiv = document.createElement("div");
        msgDiv.className = `chat-msg ${sender === "user" ? "msg-user" : "msg-shaman"}`;
        
        if (sender === "shaman") {
            msgDiv.innerHTML = `
                <div class="shaman-avatar">玄虛</div>
                <div class="msg-bubble ${isWarning ? 'bubble-warning' : ''}">
                    ${isWarning ? '⚡ <strong>[도인의 죽비 호통]</strong><br>' : ''}${formatMarkdown(text)}
                </div>
            `;
        } else {
            msgDiv.innerHTML = `
                <div class="msg-bubble user-bubble">
                    ${escapeHtml(text)}
                </div>
            `;
        }

        qaChatHistory.appendChild(msgDiv);
        qaChatHistory.scrollTop = qaChatHistory.scrollHeight;
        return msgDiv;
    }

    if (btnSendQa) {
        btnSendQa.addEventListener("click", handleSendQa);
    }

    if (qaInputText) {
        qaInputText.addEventListener("keydown", (e) => {
            if (e.key === "Enter" && !e.shiftKey) {
                e.preventDefault();
                handleSendQa();
            }
        });
    }

    async function handleSendQa() {
        const question = qaInputText.value.trim();
        if (!question) {
            showToast("도인께 여쭐 질문을 입력하십시오.");
            return;
        }

        // 금기어 사전 체크
        const taboo = checkTabooKeyword(question);
        if (taboo) {
            appendChatMessage("user", question);
            qaInputText.value = "";
            setTimeout(() => {
                appendChatMessage("shaman", `천기를 모독하는 자여! '${taboo}' 따위의 사행성 투기나 기만의 꼼수는 내 신당에서 절대 입에 올릴 수 없느니라! 당장 마음의 탐욕을 씻고 진정한 삶의 길을 묻거라!`, true);
                showToast("⚠️ 사행성/시스템 기만 금기어가 감지되었습니다.");
            }, 300);
            return;
        }

        appendChatMessage("user", question);
        qaInputText.value = "";

        const loadingMsg = appendChatMessage("shaman", "현허도인이 천기 궤적과 자미두수 별자리를 짚으며 공수를 내리고 있습니다...");
        btnSendQa.disabled = true;

        // 질문자 사주 컨텍스트 구성
        let personData = null;
        if (cachedSaju) {
            const parts = cachedSaju.solar_date.split("-");
            personData = {
                name: currentUserName || "질문자",
                year: parseInt(parts[0]),
                month: parseInt(parts[1]),
                day: parseInt(parts[2]),
                hour: 12,
                gender: "male",
                is_lunar: false
            };
        } else {
            personData = {
                name: "귀하",
                year: 1994,
                month: 3,
                day: 15,
                hour: 12,
                gender: "male",
                is_lunar: false
            };
        }

        try {
            const res = await fetch("/api/qa", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    question: question,
                    mode: selectedQaMode,
                    history: qaHistory,
                    person: personData
                })
            });

            const data = await res.json();
            if (loadingMsg) loadingMsg.remove();

            if (data.status === "success") {
                const answer = data.answer;
                appendChatMessage("shaman", answer, data.is_blocked || false);
                qaHistory.push({ role: "user", content: question });
                qaHistory.push({ role: "assistant", content: answer });
                if (qaHistory.length > 6) qaHistory = qaHistory.slice(-6); // 최근 3턴 유지
            } else {
                appendChatMessage("shaman", `천기를 읽는 도중 구름이 끼었소: ${data.message || '오류가 발생했습니다.'}`);
            }
        } catch (err) {
            if (loadingMsg) loadingMsg.remove();
            appendChatMessage("shaman", `천기와 교신이 끊겼습니다: ${err.message}`);
        } finally {
            btnSendQa.disabled = false;
        }
    }

    // 4. 출석 스탬프 리텐션 루프 (다크사주 100% 흡수)
    const STAMP_STORAGE_KEY = "cheonmyeong_stamp_data_v1";
    const stampModal = document.getElementById("stamp-modal");
    const btnOpenStamp = document.getElementById("btn-open-stamp");
    const stampCloseBtn = document.getElementById("stamp-close-btn");
    const btnDoStamp = document.getElementById("btn-do-stamp");
    const modalTicketCount = document.getElementById("modal-ticket-count");
    const headerTicketCount = document.getElementById("header-ticket-count");
    const stampCalendarGrid = document.getElementById("stamp-calendar-grid");
    const fomoCountdown = document.getElementById("stamp-fomo-countdown");

    function getStampData() {
        try {
            const raw = localStorage.getItem(STAMP_STORAGE_KEY);
            if (raw) return JSON.parse(raw);
        } catch (e) {}
        return { stampedDates: [], tickets: 1 }; // 최초 진입 시 웰컴 1회권 증정
    }

    function saveStampData(data) {
        try {
            localStorage.setItem(STAMP_STORAGE_KEY, JSON.stringify(data));
        } catch (e) {}
        updateTicketBadges(data.tickets);
    }

    function updateTicketBadges(count) {
        if (headerTicketCount) headerTicketCount.textContent = `${count}장`;
        if (modalTicketCount) modalTicketCount.textContent = `${count}장`;
    }

    function getTodayStr() {
        const d = new Date();
        const y = d.getFullYear();
        const m = String(d.getMonth() + 1).padStart(2, "0");
        const day = String(d.getDate()).padStart(2, "0");
        return `${y}-${m}-${day}`;
    }

    function renderStampCalendar() {
        if (!stampCalendarGrid) return;
        stampCalendarGrid.innerHTML = "";

        const data = getStampData();
        const todayStr = getTodayStr();
        const isTodayStamped = data.stampedDates.includes(todayStr);

        // 28일 그리드 생성
        for (let i = 1; i <= 28; i++) {
            const cell = document.createElement("div");
            cell.className = "stamp-day-cell";

            const isStamped = i <= data.stampedDates.length;
            const isTodayTarget = !isTodayStamped && i === data.stampedDates.length + 1;

            if (isStamped) {
                cell.classList.add("stamped");
                cell.innerHTML = `
                    <span class="stamp-day-num">${i}일</span>
                    <span class="stamp-cell-icon">💮</span>
                `;
            } else if (isTodayTarget) {
                cell.classList.add("today-ready");
                cell.innerHTML = `
                    <span class="stamp-day-num">${i}일</span>
                    <span class="stamp-cell-icon">📍</span>
                `;
            } else {
                cell.innerHTML = `
                    <span class="stamp-day-num">${i}일</span>
                    <span class="stamp-cell-icon">${i % 2 === 0 ? '🎁' : '⚪'}</span>
                `;
            }
            stampCalendarGrid.appendChild(cell);
        }

        if (btnDoStamp) {
            if (isTodayStamped) {
                btnDoStamp.disabled = true;
                btnDoStamp.textContent = "✅ 오늘 출석 완료 (내일 00:00 갱신)";
            } else {
                btnDoStamp.disabled = false;
                btnDoStamp.textContent = "💮 오늘의 출석 도장 찍기";
            }
        }
    }

    if (btnOpenStamp) {
        btnOpenStamp.addEventListener("click", () => {
            renderStampCalendar();
            if (stampModal) stampModal.classList.remove("hidden");
        });
    }

    if (stampCloseBtn) {
        stampCloseBtn.addEventListener("click", () => {
            if (stampModal) stampModal.classList.add("hidden");
        });
    }

    if (btnDoStamp) {
        btnDoStamp.addEventListener("click", () => {
            const data = getStampData();
            const todayStr = getTodayStr();

            if (data.stampedDates.includes(todayStr)) {
                showToast("오늘은 이미 천기 출석 도장을 찍으셨습니다.");
                return;
            }

            data.stampedDates.push(todayStr);
            const totalStamps = data.stampedDates.length;

            // 스탬프 2개당 1문 1답권 1장 지급
            let rewardMsg = "🎉 오늘 출석 도장이 성공적으로 날인되었습니다!";
            if (totalStamps % 2 === 0) {
                data.tickets += 1;
                rewardMsg = `🎉 [도장 2회 달성] 1:1 천기 심층 문답 1회권(1,200원 상당)이 즉시 지급되었습니다! (보유: ${data.tickets}장)`;
            }

            saveStampData(data);
            renderStampCalendar();
            showToast(rewardMsg);
        });
    }

    // 자정 FOMO 카운트다운 타이머
    function updateFomoCountdown() {
        if (!fomoCountdown) return;
        const now = new Date();
        const midnight = new Date(now.getFullYear(), now.getMonth(), now.getDate(), 23, 59, 59);
        const diff = midnight - now;

        if (diff > 0) {
            const hours = String(Math.floor((diff / (1000 * 60 * 60)) % 24)).padStart(2, "0");
            const minutes = String(Math.floor((diff / (1000 * 60)) % 60)).padStart(2, "0");
            const seconds = String(Math.floor((diff / 1000) % 60)).padStart(2, "0");
            fomoCountdown.textContent = `${hours}:${minutes}:${seconds}`;
        } else {
            fomoCountdown.textContent = "00:00:00";
        }
    }
    setInterval(updateFomoCountdown, 1000);
    updateFomoCountdown();

    // 초기 티켓 수치 동기화
    const initialStampData = getStampData();
    updateTicketBadges(initialStampData.tickets);

    // ==========================================================================
    // 오리지널 수묵 시네마틱 웹툰 모달 이벤트 연동
    // ==========================================================================
    const btnOpenWebtoon = document.getElementById("btn-open-webtoon");
    const webtoonModal = document.getElementById("webtoon-modal");
    const webtoonCloseBtn = document.getElementById("webtoon-close-btn");
    const btnEnterSajuFromWebtoon = document.getElementById("btn-enter-saju-from-webtoon");

    if (btnOpenWebtoon && webtoonModal) {
        btnOpenWebtoon.addEventListener("click", () => {
            webtoonModal.classList.remove("hidden");
            const modalBody = webtoonModal.querySelector(".webtoon-modal-body");
            if (modalBody) modalBody.scrollTop = 0;
        });
    }

    if (webtoonCloseBtn && webtoonModal) {
        webtoonCloseBtn.addEventListener("click", () => {
            webtoonModal.classList.add("hidden");
        });
    }

    if (btnEnterSajuFromWebtoon && webtoonModal) {
        btnEnterSajuFromWebtoon.addEventListener("click", () => {
            webtoonModal.classList.add("hidden");
            if (inputSection) inputSection.classList.remove("hidden");
            if (resultSection) resultSection.classList.add("hidden");
            const sajuForm = document.getElementById("saju-form");
            if (sajuForm) sajuForm.scrollIntoView({ behavior: "smooth" });
            showToast("🪞 도인의 거울을 통해 천명의 문이 열렸습니다. 사주를 입력하십시오.");
        });
    }

    // 모달 배경 클릭 시 닫기
    if (webtoonModal) {
        webtoonModal.addEventListener("click", (e) => {
            if (e.target === webtoonModal) {
                webtoonModal.classList.add("hidden");
            }
        });
    }

    // ==========================================================================
    // 모바일 전용 엄지손가락(Thumb Zone) 플로팅 퀵 액션 바 이벤트 바인딩
    // ==========================================================================
    const mobileFloatingBar = document.getElementById("mobile-floating-bar");
    const mfbShareInsta = document.getElementById("mfb-share-insta");
    const mfbShareKakao = document.getElementById("mfb-share-kakao");
    const mfbScrollTop = document.getElementById("mfb-scroll-top");

    window.addEventListener("scroll", () => {
        if (!mobileFloatingBar || !resultSection) return;
        const inResult = !resultSection.classList.contains("hidden");
        const scrollY = window.scrollY || window.pageYOffset;
        if (inResult && scrollY > 220) {
            mobileFloatingBar.classList.remove("hidden");
        } else {
            mobileFloatingBar.classList.add("hidden");
        }
    }, { passive: true });

    if (mfbScrollTop) {
        mfbScrollTop.addEventListener("click", () => {
            triggerHaptic(25);
            window.scrollTo({ top: 0, behavior: "smooth" });
        });
    }

    if (mfbShareInsta) {
        mfbShareInsta.addEventListener("click", () => {
            triggerHaptic(30);
            const btn = document.getElementById("btn-share-instagram");
            if (btn) btn.click();
        });
    }

    if (mfbShareKakao) {
        mfbShareKakao.addEventListener("click", () => {
            triggerHaptic(30);
            const btn = document.getElementById("btn-share-kakao");
            if (btn) btn.click();
        });
    }
});

