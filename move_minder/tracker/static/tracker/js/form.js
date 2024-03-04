const setDivWidth = () => {
    const form = document.querySelector("form");
    const formDivs = form.querySelectorAll("div");


    let setWidth = 0;
    formDivs.forEach(div => {
        div.classList.remove("block");
        div.classList.add("inline-block");
        div.removeAttribute("style");
        const maxWidth = Math.max(setWidth, div.clientWidth);
        const offset = div.offsetWidth;
        const margin = offset - div.clientWidth;
        const divParent = div.parentElement;
        setWidth = Math.min(divParent.clientWidth - margin, maxWidth)
    });

    formDivs.forEach(div => {
        div.style.width = setWidth + "px !important;";
        div.classList.remove("inline-block");
        div.classList.add("block");
    });
}

window.onload = () => {
    setDivWidth();
    const formDivs = document.querySelectorAll("form > div");
    formDivs.forEach(div => {
        const label = div.querySelector("label");
        const input = div.querySelector("input");
        if (input?.hasAttribute("required")) {
            label.classList.add("font-bold");
            const labelText = label.innerText;
            let newLabel = "";
            for (let i = 0; i < labelText.length - 1; i++) {
                newLabel += labelText[i];
            }
            newLabel += "*:";
            label.innerText = newLabel;
        }

        const errorList = div.querySelector("ul.errorlist");
        if (input && errorList) {
            input?.classList.add("invalid");
        } else {
            input?.classList.remove("invalid");
        }

        const helpText = div.querySelector(".helptext");
        if (input?.matches(":focus")) {
            helpText?.classList.remove("hidden");
            helpText?.classList.add("flex");
        } else {
            helpText?.classList.add("hidden");
            helpText?.classList.remove("flex");
        }

        input?.addEventListener("focusout", (event) => {
            if (!event.relatedTarget || !event.relatedTarget.closest('a[href]')) {
                input?.classList.remove("invalid");
                errorList?.remove();
                helpText?.classList.add("hidden");
                helpText?.classList.remove("flex");
            }
        });

        input?.addEventListener("focusin", (event) => {
            event.stopPropagation();
            helpText?.classList.remove("hidden");
            helpText?.classList.add("flex");
        });
    });
}

window.addEventListener("resize", () => setDivWidth());