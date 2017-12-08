$(function() {
	var condArr = [];

	$('.mix-select thead').each(function () {
		condArr.push([$(this).attr('class'), []]);
    });
	condArr.push(['sort', []]);

	$('.mix-select tr td').click(function() {
		var $tr = $(this).parent();
		var isChoose = $(this).children().eq(0).hasClass('active');
		var idx = $(this).parents('table').index() - 1;
		var cond = condArr[idx][1];
		var value = $(this).children().eq(0).text();

		if ($(this).index() === 0) {
			cond = [];
			$(this).children().eq(0).addClass('active');
			$.each($(this).siblings(), function (i, item) {
				$(item).children().eq(0).removeClass('active');
			});
		} else {
			$(this).siblings().eq(0).children().eq(0).removeClass('active');

			if (isChoose) {
				$(this).children().eq(0).removeClass('active');
				cond = $.grep(cond, function(item) {
 					return item !== value;
				});
			} else {
				$(this).children().eq(0).addClass('active');
				cond.push(value);
			}

			if ($tr.find('.active').length === 0) {

				$tr.find('a').eq(0).addClass('active');
			}
		}

		condArr[idx][1] = cond;
		$('.mix-select-result').text(JSON.stringify(condArr, undefined, 4));
	});

	$('.mix-select .mix-select-sort a').click(function() {
		var $div = $(this).parent();
		var isChoose = $(this).hasClass('active');
		var idx = $(this).parents('.mix-select').children('table').length;
		var cond = condArr[idx][1];
		var value = $(this).text();

		if ($(this).index() === 0) {
			cond = [];
			$(this).siblings().removeClass('active');
			$(this).addClass('active');
		} else {
			$(this).siblings().eq(0).removeClass('active');

			if (isChoose) {
				$(this).removeClass('active');
				cond = $.grep(cond, function(item) {
 					return item !== value;
				});
			} else {
				$(this).addClass('active');
				cond.push(value);
			}

			if ($div.children('.active').length === 0) {
				$div.children('a').eq(0).addClass('active');
			}
		}

		condArr[idx][1] = cond;
		$('.mix-select-result').text(JSON.stringify(condArr, undefined, 4));
	});
});



