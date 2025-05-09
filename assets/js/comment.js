var text_area = document.getElementById('input-comment')
var btn_comment = document.getElementById('btn-comment')


if (text_area.value.length > 0 ){
      btn_comment.style.display = 'flex'
}else {
      btn_comment.style.display = 'none'
}


text_area.addEventListener('focusin', () => {
      btn_comment.style.display = 'flex'
})

text_area.addEventListener('focusout', () => {
      if (! text_area.value.length > 0 ){
            btn_comment.style.display = 'none'
      }
})