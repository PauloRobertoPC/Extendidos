// Setting min-height of "main" tags
let mainMinHeight = 'calc(100vh - ' + $('#navbar').css('height') + ' - ' + $('footer').css('margin-top') + ' - ' + $('footer').css('height') + ')';
$('main').css('min-height', mainMinHeight);

// Setting "overflow: auto;" in "main" tags with "#tag-seacher" child.
if ($('main').find('#tag-searcher').length > 0) {
    $('main').css('overflow', 'auto');
}