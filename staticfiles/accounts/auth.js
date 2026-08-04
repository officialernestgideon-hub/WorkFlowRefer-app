console.log("auth.js loaded");
document.addEventListener("DOMContentLoaded", () => {

    const passwordFields = document.querySelectorAll(".password-input");

    passwordFields.forEach(field => {

        const toggle = field.parentElement.querySelector(".toggle-password");

        if (!toggle) return;

        toggle.addEventListener("click", () => {

            if (field.type === "password") {
                field.type = "text";
                toggle.innerHTML = '<i class="fa-solid fa-eye-slash"></i>';
            } else {
                field.type = "password";
                toggle.innerHTML = '<i class="fa-solid fa-eye"></i>';
            }

        });

    });

});

// ===========================
// BUSINESS LOGO PREVIEW
// ===========================

const logoInput = document.querySelector('input[type="file"]');
const logoPreview = document.getElementById("logoPreview");
const uploadText = document.getElementById("uploadText");

if (logoInput && logoPreview && uploadText) {

    logoInput.addEventListener("change", function () {

        const file = this.files[0];

        if (!file) return;

        const reader = new FileReader();

        reader.onload = function (e) {

            logoPreview.src = e.target.result;
            logoPreview.style.display = "block";

            uploadText.style.display = "none";

        };

        reader.readAsDataURL(file);

    });

}