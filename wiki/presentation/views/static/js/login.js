'use strict'


$(function() {
    let LoginButton = new IndicatorButton('#login-button')

    let View = Vue.createApp({
        delimiters: ['[[', ']]'],
        data: function() {
            return {
                user_id: '',
                password: ''
            }
        },
        methods: {
            loginButtonClick: function() {
                LoginButton.state('loading')
                $.ajax({
                    cache: false,
                    method: 'POST',
                    url: '/api/login',
                    data: {
                        user_id: this.user_id,
                        password: this.password,
                    }
                }).done((response, textStatus, jqXHR) => {
                    let date = new Date(response.expires * 1000)
                    let redirect = CookieRepository.get('redirect')
                    CookieRepository.set('redirect', '')
                    CookieRepository.set('session_id', response.session_id)
                    location.href = redirect ? redirect : '/'
                    LoginButton.state('done')
                }).fail((jqXHR, textStatus, errorThrown) => {
                    LoginButton.state('fail')
                })
            }
        }
    }).mount('#login')
})
