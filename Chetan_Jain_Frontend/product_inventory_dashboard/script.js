
var DEFAULT_PRODUCTS = [
         { id: 1, name: "Laptop", price: 55000, stock: 5, category: "electronics" },
      { id: 2, name: "Headphones", price: 2500, stock: 12, category: "electronics" },
      { id: 3, name: "T-Shirt", price: 799, stock: 30, category: "clothing" },
    { id: 4, name: "JavaScript: The Good Parts", price: 450, stock: 0, category: "books" },
     { id: 5, name: "Wrist Watch", price: 3200, stock: 3, category: "accessories" },
       { id: 6, name: "Smartphone", price: 18000, stock: 8, category: "electronics" },
    { id: 7, name: "Jeans", price: 1500, stock: 0, category: "clothing" },
    { id: 8, name: "Backpack", price: 1200, stock: 15, category: "accessories" },
       { id: 9, name: "Python Crash Course", price: 600, stock: 2, category: "books" },
      { id: 10, name: "Bluetooth Speaker", price: 3500, stock: 4, category: "electronics" },
    { id: 11, name: "Sunglasses", price: 900, stock: 20, category: "accessories" },
        { id: 12, name: "Hoodie", price: 1800, stock: 7, category: "clothing" }
];

var PRODUCTS_PER_PAGE = 6;



var products = [];         
var filteredProducts = [];  
var currentPage = 1;        


var searchInput = document.getElementById("search-input");
var categoryFilter = document.getElementById("category-filter");
var sortSelect = document.getElementById("sort-select");
var lowStockToggle = document.getElementById("low-stock-toggle");
var productGrid = document.getElementById("product-grid");
var addProductForm = document.getElementById("add-product-form");
var loadingOverlay = document.getElementById("loading-overlay");


var totalProductsEl = document.getElementById("total-products");
var totalValueEl = document.getElementById("total-value");
var outOfStockEl = document.getElementById("out-of-stock");

var pageInfoEl = document.getElementById("page-info");
var pageNumbersEl = document.getElementById("page-numbers");
var prevPageBtn = document.getElementById("prev-page-btn");
var nextPageBtn = document.getElementById("next-page-btn");
var pageInfoBottomEl = document.getElementById("page-info-bottom");
var pageNumbersBottomEl = document.getElementById("page-numbers-bottom");
var prevPageBtnBottom = document.getElementById("prev-page-btn-bottom");
var nextPageBtnBottom = document.getElementById("next-page-btn-bottom");
var nameInput = document.getElementById("product-name");
var priceInput = document.getElementById("product-price");
var stockInput = document.getElementById("product-stock");
var categoryInput = document.getElementById("product-category");

var nameError = document.getElementById("name-error");
var priceError = document.getElementById("price-error");
var stockError = document.getElementById("stock-error");
var categoryError = document.getElementById("category-error");



function saveToLocalStorage() {
    localStorage.setItem("inventoryProducts", JSON.stringify(products));
}


function loadFromLocalStorage() {
    var data = localStorage.getItem("inventoryProducts");
    if (data) {
        return JSON.parse(data);
    }
    return null;
}


//api call

function fetchProducts() {
    return new Promise(function (resolve) {
        
        var savedProducts = loadFromLocalStorage();

        
        setTimeout(function () {
            if (savedProducts && savedProducts.length > 0) {
                resolve(savedProducts);
            } else {
                
                resolve(DEFAULT_PRODUCTS);
            }
        }, 1500);
    });
}


//analytics

function updateAnalytics() {
    var totalCount = products.length;

    
    var totalValue = 0;
    for (var i = 0; i < products.length; i++) {
        totalValue += products[i].price * products[i].stock;
    }

    
    var outOfStock = 0;
    for (var i = 0; i < products.length; i++) {
        if (products[i].stock === 0) {
            outOfStock++;
        }
    }

    
    totalProductsEl.textContent = totalCount;
    totalValueEl.textContent = "₹" + totalValue.toLocaleString("en-IN");
    outOfStockEl.textContent = outOfStock;
}


//filtering
function applyFiltersAndSort() {
    var searchTerm = searchInput.value.trim().toLowerCase();
    var selectedCategory = categoryFilter.value;
    var showLowStockOnly = lowStockToggle.checked;
    var sortOption = sortSelect.value;

   
    var result = products.slice();

    
    if (searchTerm !== "") {
        result = result.filter(function (product) {
            return product.name.toLowerCase().indexOf(searchTerm) !== -1;
        });
    }

   
    if (selectedCategory !== "all") {
        result = result.filter(function (product) {
            return product.category === selectedCategory;
        });
    }

    if (showLowStockOnly) {
        result = result.filter(function (product) {
            return product.stock < 5;
        });
    }

   
    if (sortOption === "price-low-high") {
        result.sort(function (a, b) {
            return a.price - b.price;
        });
    } else if (sortOption === "price-high-low") {
        result.sort(function (a, b) {
            return b.price - a.price;
        });
    } else if (sortOption === "name-az") {
        result.sort(function (a, b) {
            return a.name.toLowerCase().localeCompare(b.name.toLowerCase());
        });
    } else if (sortOption === "name-za") {
        result.sort(function (a, b) {
            return b.name.toLowerCase().localeCompare(a.name.toLowerCase());
        });
    }

    filteredProducts = result;

    
    currentPage = 1;

    renderProducts();
    renderPagination();
}


//product rendering

function renderProducts() {
    
    productGrid.innerHTML = "";
if (filteredProducts.length === 0) {
        var msgDiv = document.createElement("div");
        msgDiv.className = "no-products-msg";
        msgDiv.innerHTML = "No products found. ";
        productGrid.appendChild(msgDiv);
        return;
    }

    var startIndex = (currentPage - 1) * PRODUCTS_PER_PAGE;
    var endIndex = startIndex + PRODUCTS_PER_PAGE;
    var pageProducts = filteredProducts.slice(startIndex, endIndex);
for (var i = 0; i < pageProducts.length; i++) {
        var product = pageProducts[i];
        var card = createProductCard(product);
        productGrid.appendChild(card);
    }
}


function createProductCard(product) {
    var card = document.createElement("div");
    card.className = "product-card " + product.category;
    card.setAttribute("data-id", product.id);

  
    var nameEl = document.createElement("h3");
    nameEl.className = "product-name";
    nameEl.textContent = product.name;


    var categoryEl = document.createElement("span");
    categoryEl.className = "product-category";
    categoryEl.textContent = product.category;


    var infoDiv = document.createElement("div");
    infoDiv.className = "product-info";

    var priceEl = document.createElement("span");
    priceEl.className = "product-price";
    priceEl.textContent = "₹" + product.price.toLocaleString("en-IN");

    var stockEl = document.createElement("span");
    stockEl.className = "product-stock";

   
    if (product.stock === 0) {
        stockEl.textContent = "Out of Stock";
        stockEl.classList.add("out-of-stock");
    } else if (product.stock < 5) {
        stockEl.textContent = "Stock: " + product.stock + " (Low)";
        stockEl.classList.add("low-stock");
    } else {
        stockEl.textContent = "Stock: " + product.stock;
    }

    infoDiv.appendChild(priceEl);
    infoDiv.appendChild(stockEl);

  
    var deleteBtn = document.createElement("button");
    deleteBtn.className = "btn-delete";
    deleteBtn.textContent = "Delete";
   
    deleteBtn.addEventListener("click", function () {
        deleteProduct(product.id);
    });

    
    card.appendChild(nameEl);
    card.appendChild(categoryEl);
    card.appendChild(infoDiv);
    card.appendChild(deleteBtn);

    return card;
}


//pagination

function renderPagination() {
    var totalPages = Math.ceil(filteredProducts.length / PRODUCTS_PER_PAGE);

    
    if (totalPages <= 1) {
        document.getElementById("pagination-bar").style.display = "none";
        document.getElementById("pagination-bar-bottom").style.display = "none";
        return;
    }

    document.getElementById("pagination-bar").style.display = "flex";
    document.getElementById("pagination-bar-bottom").style.display = "flex";

   
    var start = (currentPage - 1) * PRODUCTS_PER_PAGE + 1;
    var end = Math.min(currentPage * PRODUCTS_PER_PAGE, filteredProducts.length);
    var infoText = "Showing " + start + "-" + end + " of " + filteredProducts.length + " products";

    pageInfoEl.textContent = infoText;
    pageInfoBottomEl.textContent = infoText;

    
    prevPageBtn.disabled = (currentPage === 1);
    nextPageBtn.disabled = (currentPage === totalPages);
    prevPageBtnBottom.disabled = (currentPage === 1);
    nextPageBtnBottom.disabled = (currentPage === totalPages);

    buildPageNumbers(pageNumbersEl, totalPages);
    buildPageNumbers(pageNumbersBottomEl, totalPages);
}


function buildPageNumbers(container, totalPages) {
    container.innerHTML = "";

    for (var i = 1; i <= totalPages; i++) {
        var pageBtn = document.createElement("span");
        pageBtn.className = "page-num";
        pageBtn.textContent = i;

        if (i === currentPage) {
            pageBtn.classList.add("active");
        }

        (function (pageNum) {
            pageBtn.addEventListener("click", function () {
                currentPage = pageNum;
                renderProducts();
                renderPagination();
               
                window.scrollTo({ top: productGrid.offsetTop - 100, behavior: "smooth" });
            });
        })(i);

        container.appendChild(pageBtn);
    }
}


function goToPrevPage() {
    if (currentPage > 1) {
        currentPage--;
        renderProducts();
        renderPagination();
        window.scrollTo({ top: productGrid.offsetTop - 100, behavior: "smooth" });
    }
}


function goToNextPage() {
    var totalPages = Math.ceil(filteredProducts.length / PRODUCTS_PER_PAGE);
    if (currentPage < totalPages) {
        currentPage++;
        renderProducts();
        renderPagination();
        window.scrollTo({ top: productGrid.offsetTop - 100, behavior: "smooth" });
    }
}



function generateId() {
    return Date.now() + Math.floor(Math.random() * 1000);
}


function handleAddProduct(event) {
    event.preventDefault();

    
    clearFormErrors();

    var name = nameInput.value.trim();
    var price = priceInput.value.trim();
    var stock = stockInput.value.trim();
    var category = categoryInput.value;

    var isValid = true;

    
    if (name === "") {
        showError(nameInput, nameError, "Product name is required.");
        isValid = false;
    }


    if (price === "" || isNaN(price) || parseFloat(price) <= 0) {
        showError(priceInput, priceError, "Price must be a number greater than 0.");
        isValid = false;
    }

    
    if (stock === "" || isNaN(stock) || parseInt(stock) < 0) {
        showError(stockInput, stockError, "Stock cannot be negative.");
        isValid = false;
    }

    
    if (category === "") {
        showError(categoryInput, categoryError, "Please select a category.");
        isValid = false;
    }

 
    if (!isValid) {
        return;
    }

    
    var newProduct = {
        id: generateId(),
        name: name,
        price: parseFloat(price),
        stock: parseInt(stock),
        category: category
    };

   
    products.push(newProduct);

    
    saveToLocalStorage();

   
    updateAnalytics();
    applyFiltersAndSort();


    addProductForm.reset();
}


function showError(inputEl, errorEl, message) {
    inputEl.classList.add("invalid");
    errorEl.textContent = message;
}


function clearFormErrors() {
    nameInput.classList.remove("invalid");
    priceInput.classList.remove("invalid");
    stockInput.classList.remove("invalid");
    categoryInput.classList.remove("invalid");
    nameError.textContent = "";
    priceError.textContent = "";
    stockError.textContent = "";
    categoryError.textContent = "";
}


function deleteProduct(productId) {
  
    var confirmDelete = confirm("Are you sure you want to delete this product?");
    if (!confirmDelete) {
        return;
    }

   
    products = products.filter(function (product) {
        return product.id !== productId;
    });

    
    saveToLocalStorage();
    updateAnalytics();
    applyFiltersAndSort();
}



searchInput.addEventListener("input", function () {
    applyFiltersAndSort();
});


categoryFilter.addEventListener("change", function () {
    applyFiltersAndSort();
});


sortSelect.addEventListener("change", function () {
    applyFiltersAndSort();
});


lowStockToggle.addEventListener("change", function () {
    applyFiltersAndSort();
});

addProductForm.addEventListener("submit", handleAddProduct);


prevPageBtn.addEventListener("click", goToPrevPage);
nextPageBtn.addEventListener("click", goToNextPage);
prevPageBtnBottom.addEventListener("click", goToPrevPage);
nextPageBtnBottom.addEventListener("click", goToNextPage);


nameInput.addEventListener("input", function () {
    nameInput.classList.remove("invalid");
    nameError.textContent = "";
});
priceInput.addEventListener("input", function () {
    priceInput.classList.remove("invalid");
    priceError.textContent = "";
});
stockInput.addEventListener("input", function () {
    stockInput.classList.remove("invalid");
    stockError.textContent = "";
});
categoryInput.addEventListener("change", function () {
    categoryInput.classList.remove("invalid");
    categoryError.textContent = "";
});




function disableControls() {
    searchInput.disabled = true;
    categoryFilter.disabled = true;
    sortSelect.disabled = true;
    lowStockToggle.disabled = true;
    addProductForm.querySelector(".btn-add").disabled = true;
}

function enableControls() {
    searchInput.disabled = false;
    categoryFilter.disabled = false;
    sortSelect.disabled = false;
    lowStockToggle.disabled = false;
    addProductForm.querySelector(".btn-add").disabled = false;
}

function initApp() {
    // Show loading state
    
setTimeout(function () {
    loadingOverlay.classList.add("hidden");
}, 50);
    disableControls();

    // Fetch products 
    fetchProducts().then(function (loadedProducts) {
       
        products = loadedProducts;

        
        saveToLocalStorage();

        // Calculate analytics
        updateAnalytics();

     
        applyFiltersAndSort();

        
        loadingOverlay.classList.add("hidden");

        
        enableControls();
    });
}


initApp();