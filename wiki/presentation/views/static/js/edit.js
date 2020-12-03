'use strict'

$(function() {
    let SubmitButton = new IndicatorButton('#edit-submit')

    let View = Vue.createApp({
        delimiters: ['[[', ']]'],
        data: function() {
            return {
                markedJsTimer: null,
                codeMirror: null,
                page: {
                    page_id: '',
                    title: '',
                    body: '',
                    lastmodified: 0,
                    version: 0
                }
            }
        },
        mounted: function() {
            this.getPage()
        },
        methods: {
            updateMarkdownPreview: function() {
                $('#markdown-preview').html(marked(this.codeMirror.getValue()))
                document.querySelectorAll('pre code').forEach((block) => {
                    hljs.highlightBlock(block)
                })
            },
            updateMarkdownPreviewDelay: function() {
                if(this.markedJsTimer)
                    clearTimeout(this.markedJsTimer)
                this.markedJsTimer = setTimeout(() => {
                    this.updateMarkdownPreview()
                    this.markedJsTimer = null
                }, 1000)
            },
            getPage: function() {
                $.ajax({
                    cache: false,
                    method: 'GET',
                    url: '/api/page' + new URL(location.href).pathname
                }).done((response) => {
                    let editor = $('#markdown-editor').text(response.body)
                    this.page = response
                    this.codeMirror = CodeMirror.fromTextArea(editor[0], {
                        mode: 'markdown',
                        theme: 'paraiso-dark',
                        autoFocus: true,
                        lineNumbers: true,
                        lineWrapping: true,
                        smartIndent: true
                    })
                    this.codeMirror.on('changes', this.updateMarkdownPreviewDelay)
                    this.updateMarkdownPreview()
                })
            },
            submitButtonClick: function() {
                SubmitButton.state('loading')
                $.ajax({
                    cache: false,
                    method: 'POST',
                    url: '/api/page/' + this.page.page_id,
                    data: {
                        title: this.page.title,
                        version: this.page.version,
                        body: this.codeMirror.getValue(),
                    }
                }).done((response) => {
                    this.page = response
                    $('#page-version').val(response.version)
                    SubmitButton.state('done')
                }).fail(() => {
                    SubmitButton.state('fail')
                })
            }
        }
    }).mount('#edit')
})
