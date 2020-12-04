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


let CookieRepository = {
    get: function(key) {
        let pairs = document.cookie.split('; ')
        for(let i = 0; i < pairs.length; i++) {
            let pair = pairs[i].split('=')
            if(pair[0] == key)
                return pair[1]
        }
        return null
    },
    set: function(key, value) {
        document.cookie = key + '=' + value + ';';
    },
    setIfAbsent: function(key, value) {
        if(!this.get(key))
            this.set(key, value)
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
        let redirect = CookieRepository.get('redirect')
        CookieRepository.set('redirect', '')
        location.href = redirect ? redirect : '/'
    })
    $('#login-menu-edit').on('click', () => {
        let path = new URL(location.href).pathname
        CookieRepository.setIfAbsent('redirect', path)
        location.href = '?edit=1'
    })
    $('#login-menu-profile').on('click', () => {
        let path = new URL(location.href).pathname
        CookieRepository.setIfAbsent('redirect', path)
        location.href = '/profile'
    })
    $('#login-menu-manage').on('click', () => {
        let path = new URL(location.href).pathname
        CookieRepository.setIfAbsent('redirect', path)
        location.href = '/manage'
    })
    $('#login-menu-logout').on('click', () => {
        document.cookie = 'session_id=; expires=' + (new Date().toGMTString())
        let redirect = CookieRepository.get('redirect')
        CookieRepository.set('redirect', '')
        location.href = redirect ? redirect : '/'
    })
})
