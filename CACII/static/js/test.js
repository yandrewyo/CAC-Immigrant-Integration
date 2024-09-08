pdfjsLib.GlobalWorkerOptions.workerSrc = "https://cdn.jsdelivr.net/npm/pdfjs-dist@2.7.570/build/pdf.worker.min.js"


function goToPage(title) {
    const pdfElem = document.getElementById("pdf-view")
    const pdfUrl = pdfElem.src;

    pdfjsLib.getDocument(pdfUrl).promise.then(function (pdf) {
        const numPages = pdf.numPages;

        function getPageText(pageNum) {
            return pdf.getPage(pageNum).then(function (page) {
                return page.getTextContent();
            }).then(function (text) {
                return text.items.map(item => item.str).join(' ');
            })
        }
        for (let i = 1; i <= numPages; i++) {
            getPageText(i).then(function (text) {
                if (text.includes(title)) {
                    // pdfElem.src = pdfElem.getAttribute("src")+`#page=${i}`
                    pdfElem.src = pdfUrl.slice(pdfUrl.indexOf("static")-1, pdfUrl.indexOf("pdf")+3)+`#page=${i}`
                }
            })
        }
    })
}

document.addEventListener("DOMContentLoaded", function(){
    const li = document.getElementsByTagName("li")
    for (let i = 0; i < li.length; i++) {
        // let teststring = {{module_file_name|escapejs}}
        // console.log(teststring);
        li[i].addEventListener("click", function () {
            goToPage(li[i].innerText);
        })
    }
});