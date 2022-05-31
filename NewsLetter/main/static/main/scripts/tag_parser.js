posts = $("*#text")
$(posts).each(function (index,post) {
    let words = post.innerText.split(" ")
    $(words).each(function (index,word) {
        if (word.indexOf('#') != -1) {
            url_word = word.substring(1)
            $(post).html($(post).html().replace(word, `<a class='tag-word' href="main?tag=` + url_word + `">` + word + `</a>` ))
        }
    })
})