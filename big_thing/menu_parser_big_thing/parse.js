var request = require('request');
var cheerio = require('cheerio');
var fs = require('fs');

var date = new Date();
var url = 'http://mini.snu.kr/cafe/set/2021-' + (date.getMonth() + 1) + '-' + date.getDate();

var menustr = (date.getMonth() + 1) + '월 ' + date.getDate() + '일';

function parse(lunch){
    console.log(url)

    if(lunch == 1)
        menustr += ' 점심 메뉴입니다.\n';
    else
        menustr += ' 저녁 메뉴입니다.\n';
    request(url, function (error, response, body) {
        console.log(body)
        if(error) throw error;

        var $ = cheerio.load(body);
        var isLunch = false;
        var isDinner = false;

        $('tr').each(function() {
            var time = $(this).text();
            if(time == '점심'){
                isLunch = true;
                return;
            }
            else if(time == '저녁'){
                isLunch = false;
                isDinner = true;
                return;
            }

            var place = $(this).find('td.bg_menu2').text();
            var menu = $(this).find('td.menu').text();

            console.log(menu)

            if(((isLunch && lunch == '1') || (isDinner && lunch == '0')) && (place == '301동' || place == '302동')){
                if(menu == '')
                {
                    menu = '없습니다'
                }
                else
                {
                    menu = menu.replace(/(\d{2})(\d{0,3}\D+)/g, '$2 $100원\n');
                    menu = menu.replace(/\&/g, ' ');
                    menu = menu.replace(/4종소스\(선택1\)\n/, '');
                }
                menustr += place + '\n' + menu;
                console.log('직전1')
                console.log(menustr)
            }
        });     
    
        console.log('직전2')
        console.log(menustr)
        fs.writeFile('./menu.txt', menustr, function(err){
            if(err) throw err;
            console.log('menu write completed');
        });
    });
};

parse(process.argv[2]);
