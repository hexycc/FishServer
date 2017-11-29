$(function() {

    String.prototype.lengthB = function( ){
        var b = 0, l = this.length;
        if( l ){
            for( var i = 0; i < l; i ++ ){
                if(this.charCodeAt( i ) > 255 ){
                    b += 2;
                }else{
                    b ++ ;
                }
            }
            return b;
        }else{
            return 0;
        }
    }

    $('.tijiao').on('touchend', tijiao)

    // var tbimg = 'http://zhuangbi.zuihaokanapp.com/zb/pyqzd/icon.jpg'
    var mask = 'background.jpg'

    function tijiao(){

        var text = $('.input-sty').val()
        var imgData = $('.pa-preview').attr('src');
        if(imgData === 'cover.jpg'){
            alert('请添加照片')
            return
        }

       creatCanvas(imgData, text);

       window.scrollTo(0,0)

    }

    var ratio = window.devicePixelRatio

    function creatCanvas(imgData,text){

        $('input').blur()

        $('.result-page').show()

        var C = document.createElement('canvas')
        var cvs = C.getContext("2d")
        C.width = 960
        C.height = 1280

        var img = new Image();
        img.src = imgData;

        img.onload = function(){

            var maskimg = new Image()
            maskimg.src = 'background.png'

            maskimg.onload = function () {
                var iw = img.width
                var ih = img.height

                var cw = C.width
                var ch = C.height

                var aw
                var ah
                var lp

                if(iw<ih){ //长图
                    aw = 240
                    ah = aw*ih/iw
                    if(ah < 418){
                        ah = 418
                        aw = ah*iw/ih
                        lp = 360 - (aw-240)/2
                    }
                }else{ //宽图
                    ah = 418
                    aw = ah*iw/ih
                    lp = 360 - (aw-240)/2
                }

                

                cvs.drawImage(img,lp,465,aw,ah)
                cvs.drawImage(maskimg,0,0,cw,ch)

                // cvs.fillStyle = '#ff6600'
                // cvs.font = 40+'px arial'

                // var l = text.lengthB()

                // var left = cw/2 - 12*l/2
                // cvs.fillText(text, 10, 895)

                var imgsrc = C.toDataURL("image/jpg")

                $('.result-page').find('img').attr('src', imgsrc)

                var rh = $('.result-page').height() - 20

                $('.content').height(rh)

                $('#title_header h1').html('长按下方图片点选保存图片');                
            }

        }

        
    }

    var reader = function(file, option){

        var option = option || {}

        return new Promise(function(resolve, reject){

            var reader = new FileReader()

            reader.onload = function(){
                resolve(reader)
            }

            reader.onerror = function(){
                reject()
            }

            reader.readAsDataURL(file)
        })
    }

    $('.J_filebtn').on('change', function(e){

        var file = $(this).prop('files')[0]

        reader(file).then(function(reader){

            $('.pa-preview').attr('src', reader.result)

            // $('.pa-preview').find('input').hide()

            // $('.btn-huan').show().find('input').on('touchend', function(e){
            //  $(this).attr('name', 'file')
            //  $('.pa-preview').find('input').remove()
            // })

        }, function(){

            alert('操作失败，请重试！')

        })

    })

})
