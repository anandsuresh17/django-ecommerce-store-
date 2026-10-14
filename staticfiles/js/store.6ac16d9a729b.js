
document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("filterForm");
    const searchInput = document.getElementById("productSearch");
    const categoryFilter = document.getElementById("categoryFilter");
    const minPriceInput = document.getElementById("minPrice");
    const maxPriceInput = document.getElementById("maxPrice");
    const clearButton = document.getElementById("clearFilters");
    const resultCount = document.getElementById("resultCount");

    const productCards = Array.from(
        document.querySelectorAll(".product-card[data-price]")
    );

    function filterProducts() {
        const searchTerm = searchInput.value.trim().toLowerCase();
        const selectedCategory = categoryFilter.value;
        const minPrice = minPriceInput.value === ""
            ? null
            : Number(minPriceInput.value);
        const maxPrice = maxPriceInput.value === ""
            ? null
            : Number(maxPriceInput.value);

        let visibleCount = 0;

        productCards.forEach(function (card) {
            const name = card.dataset.name || "";
            const description = card.dataset.description || "";
            const category = card.dataset.category || "";
            const price = Number(card.dataset.price);

            const matchesSearch =
                name.includes(searchTerm) ||
                description.includes(searchTerm);

            const matchesCategory =
                selectedCategory === "" ||
                category === selectedCategory;

            const matchesMinPrice =
                minPrice === null || price >= minPrice;

            const matchesMaxPrice =
                maxPrice === null || price <= maxPrice;

            const isVisible =
                matchesSearch &&
                matchesCategory &&
                matchesMinPrice &&
                matchesMaxPrice;

            card.hidden = !isVisible;

            if (isVisible) {
                visibleCount++;
            }
        });

        resultCount.textContent =
            `Showing ${visibleCount} of ${productCards.length} products`;

        let emptyMessage = document.getElementById("noProductsMessage");

        if (visibleCount === 0) {
            if (!emptyMessage) {
                emptyMessage = document.createElement("p");
                emptyMessage.id = "noProductsMessage";
                emptyMessage.className = "empty-message";
                emptyMessage.textContent =
                    "No products match your search or filters.";

                const grid = document.querySelector(".product-grid");

                if (grid) {
                    grid.appendChild(emptyMessage);
                }
            }
        } else if (emptyMessage) {
            emptyMessage.remove();
        }
    }

    // Prevent the form from reloading the page.
    form.addEventListener("submit", function (event) {
        event.preventDefault();
        filterProducts();
    });

    // Filter as the user types or changes a filter.
    searchInput.addEventListener("input", filterProducts);
    categoryFilter.addEventListener("change", filterProducts);
    minPriceInput.addEventListener("input", filterProducts);
    maxPriceInput.addEventListener("input", filterProducts);

    clearButton.addEventListener("click", function () {
        searchInput.value = "";
        categoryFilter.value = "";
        minPriceInput.value = "";
        maxPriceInput.value = "";

        filterProducts();
    });

    filterProducts();
});
