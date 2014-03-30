"use strict";
angular.module('vk').directive('vkPostText', function($sanitize) {
  var maxWords = 40;

  return {
    restrict: 'A',
    scope: {
      text: '=vkPostText'
    },
    compile: function(element, attrs, transclude) {
      return function(scope, element, attrs, controller) {
        var text = (scope.text || '').split('  ').join(' ');
        var sliced = text.split(' ');

        var firstPart = text; 
        var secondPart = '';

        if (sliced.length > maxWords) {
            firstPart = '';
            for (var i = 0; i < maxWords; i++) {
                firstPart += sliced[i] + ' ';
            }
            for (i = maxWords; i < sliced.length;i++) {
                secondPart += sliced[i] + ' ';
            }
        }

        var uniqueId = Math.random().toString();
        var result = '<div class="post-text">';

        firstPart = $sanitize(firstPart);
        secondPart = $sanitize(secondPart);

        if(secondPart !== '') {
            result = firstPart + 
                      '<span data-id="' + uniqueId + '" class="read-more-link" onclick="this.style.display = \'none\'; document.getElementById(\'read-more-\' + this.getAttribute(\'data-id\')).style.display=\'block\';">читать дальше...</span>' + 
                      '<span class="read-more" id="read-more-' + uniqueId + '">' + 
                        secondPart + 
                      '</span>';
        } else {
            result = text;
        }

        element[0].innerHTML = result;
      }
    }
  }
}).directive('vkPostAttachments', function() {
  var Renderer = {
    getAttachmentsHtml : function(attachments) {
        attachments = attachments || [];
        
        //обрабатываем аттачи с фотками
        var resultHtml = '', 
            photoHtml = '',
            audioHtml = '',
            videoHtml = '',
            docHtml = '';

        if (attachments.length > 0) {
            var photoCnt = 0;
            photoHtml =  Renderer.photoAttachmentsProccess(attachments, "photo", function (att) {
                var res = Renderer.processPhoto(photoHtml, photoCnt, att);
                photoCnt++;
                return res;
            });
            audioHtml = Renderer.photoAttachmentsProccess(attachments, "audio", function (att) {
                return '<div class="audio_item">' + att.audio.performer + ' - ' + att.audio.title + '</div>';
            });
              
            videoHtml = Renderer.photoAttachmentsProccess(attachments, "video", function (att) {
                var vsrc = photoCnt == 0 ? att.video.image_big : att.video.image_small;
                var maxHintLenght = photoCnt == 0 ? 50 : 13;
                var vhint = att.video.title.length > maxHintLenght ? att.video.title.substring(0, maxHintLenght) + '...' : att.video.title;
                photoCnt++;
                
                return '<div class="photo-item">' +
                    '<a href=http://vk.com/video' + att.video.owner_id + '_' + att.video.vid + '>' +
                    '<img src="' + vsrc + '"></a>' +
                    (photoCnt == 0 ? '<div class="video_item_title">' + vhint + '</div>' : '') +
                    '</div>';
                //return '<div class="audio_item">' + att.audio.performer + ' - ' + att.audio.title + '</div>';
            });

            docHtml = Renderer.photoAttachmentsProccess(attachments, "doc", function (att) {
                return '<div class="doc_item">' +
                    '<a href=http://vk.com/doc' + att.doc.owner_id + '_' + att.doc.did + '>' +
                    '<img src="' + att.doc.thumb_s + '"></a>' +
                    '<div class="doc_item_title">' + att.doc.title + '</div>' +
                    '</div>';
            });
        }
        
        var postId = Math.random().toString();

        if (photoHtml || videoHtml) {
            resultHtml += '<div class="photo-container" id="photo-container' + postId + '" data-masonry-options=\'{ "columnWidth": 200, "itemSelector": ".photo-item" }\' \>' + photoHtml + videoHtml + "</div>";
            Renderer.photoContainers.push('photo-container' + postId);
        }
        if (docHtml) {
            resultHtml += '<div class="doc-container" id="doc-container' + postId + '">' + docHtml + "</div>";
        }
        if (audioHtml) {
          resultHtml += '<div class="audio-container" id="audio-container' + postId + '">' + audioHtml + "</div>";
        }

        return resultHtml;
    },

    photoAttachmentsProccess: function (attachments, type,  func ) {
        var resHtml = '';
        attachments.forEach(function (att) {
            if (att.type == type)
                resHtml += func(att);
        });
        return resHtml;
    },

    //обработка аттача с фоткой
    processPhoto : function(curHtml, photoCnt, att) {
        var mclass = 'photo-item';
        var photoHtml = curHtml;
        if (photoCnt > 0)
            mclass = 'photo-item w2';
        var photoSrc = photoCnt == 0 ? att.photo.src_big : att.photo.src;
        photoHtml += '<div class="' + mclass + '" ><a href="http://vk.com/photo' + att.photo.owner_id + '_' + att.photo.pid + '" target="_blank"><img src="' + photoSrc + '"/></a></div>';
        return photoHtml;
    },

    photoContainers : ['abc']
  };

  return {
    restrict: 'A',
    scope: {
      attachments: '=vkPostAttachments'
    },
    compile: function(element, attrs, transclude) {
      return function(scope, element, attrs, controller) {
        element[0].innerHTML = Renderer.getAttachmentsHtml(scope.attachments);
      }
    }
  };
});
