'use strict'


let IndicatorButton = function(selector) {
    this.selector = selector
    this.timerId = null
}

IndicatorButton.prototype.state = function(state) {
    $(this.selector).removeClass('waiting loading done fail').addClass(state)
    if(state == 'done' || state == 'fail') {
        if(this.timerId)
            clearTimeout(this.timerId)
        this.timerId = setTimeout(() => this.state('waiting'), 2000)
    }
}


$(function() {
    let source = $('#markdown-source').html()
    if(source) {
        $('#markdown-preview').html(marked(source))
        document.querySelectorAll('pre code').forEach((block) => {
            hljs.highlightBlock(block)
        })
    }

    $('#login-menu-view').on('click', () => {
        let redirect = new URL(location.href).searchParams.get('redirect')
        location.href = '/' + (redirect ? redirect : '')
    })
    $('#login-menu-edit').on('click', () => {
        let path = new URL(location.href).pathname.substring(1)
        location.href = '?edit=1&redirect=' + path
    })
    $('#login-menu-profile').on('click', () => {
        let path = new URL(location.href).pathname.substring(1)
        location.href = '/profile?redirect=' + path
    })
    $('#login-menu-manage').on('click', () => {
        let path = new URL(location.href).pathname.substring(1)
        location.href = '/manage?redirect=' + path
    })
    $('#login-menu-logout').on('click', () => {
        document.cookie = 'session_id=; expires=' + (new Date().toGMTString())
        location.href = '/'
    })
})
