// 'http://localhost:5000/'
const baseUrl = 'https://bak-ocr-project.herokuapp.com/'

function atualizaLinkCamera(link) {
    if (['', '.'].includes(link)){
        return ''
    }

    let complementoInicio = ""
    let complementoFim =""

    if (!link.startsWith("http://")){
        complementoInicio = "http://"
    }
    if (link.endsWith("/")) {
        complementoFim = "video"
    } else if (!link.endsWith("/video")) {
        complementoFim = "/video"
    }

    return `${complementoInicio}${link}${complementoFim}`
}

function mostraAlerta(tipo, mensagem, destaque) {
    let classes = $("#alerta-principal").attr('class')
    let classe_a_remover = /alert-(warning|success|info)/.exec(classes)[0]
    $("#alerta-principal").removeClass(classe_a_remover)
    $("#alerta-principal").addClass(`alert-${tipo}`)
        
    $("#alerta-principal p").text(mensagem)
    $("#alerta-principal p").prepend($("<strong>").text(destaque))

    $('#alerta-principal').removeAttr('hidden');

    setTimeout(function () {
        $('#alerta-principal').attr('hidden', 'true');
    }, 4000);
}

const alertaUsuario = {
    info: (mensagem) => {
        mostraAlerta('info', mensagem, 'Info! ')
    },
    aviso: (mensagem) => {
        mostraAlerta('warning', mensagem, 'Aviso! ')
    },
    sucesso: (mensagem) => {
        mostraAlerta('success', mensagem, 'Feito! ')
    }
}

function trocaVisibilidadeCamera(){
    if ($("#area-entrada-link").is(':visible') == true){
        $("#area-entrada-link").hide()
    } else {
        $("#area-entrada-link").show()
    }
}

function trocaVisibilidadeCampoLink(){
    if ($("#area-camera").is(':visible') == true){
        $("#area-camera").hide()
    } else {
        $("#area-camera").show()
    }
}

function alternaVisibilidadeLinkComCamera(){
    trocaVisibilidadeCamera()
    trocaVisibilidadeCampoLink()
}

$('#botao-abrir-camera').on('click', (event) => {
    event.preventDefault();

    let linkCamera = atualizaLinkCamera($("#campo-link-camera").val());
    
    if (linkCamera) {
        let linkTeste = linkCamera.replace('video', '')
        $.ajax({
            url: linkTeste,
            success: function (response) {
                $("#camera").attr('src', linkCamera)
                alternaVisibilidadeLinkComCamera()
            },
            error: function (xhr, status) {
                console.log('>>', xhr)
                console.log('>>>', status)
                alertaUsuario.aviso('Link Indisponível')
            }
        });
    } else {
        alertaUsuario.info('Insira um link válido no campo.')
        $("#campo-link-camera")[0].focus()
    }
})

$('#salvar-imagem').on('click', (event) => {
    linkCamera = $('#camera').attr('src')
    if (linkCamera){
        linkImagem = linkCamera.replace('video', 'photo.jpg')
        $.post(baseUrl + 'salvar-imagem', {'link_imagem': linkImagem})
        .done((resp) => {
            console.log(resp)
            alertaUsuario.sucesso(`Tudo em ordem`)
            $("#camera").attr('src', '')
            $("#campo-link-camera").val('')
            alternaVisibilidadeLinkComCamera()
        })
        .fail((resp) => {
            console.log(resp)
            alertaUsuario.aviso(`Algo de errado aconteceu. Contate o suporte ou tente novamente.`)
        })
    } else {
        alertaUsuario.aviso('Nenhuma camera disponivel')
    }
})

$('#botao-fechar-camera').on('click', () => {
    $("#camera").attr('src', '')
    alternaVisibilidadeLinkComCamera()
    $("#campo-link-camera")[0].focus()
})

