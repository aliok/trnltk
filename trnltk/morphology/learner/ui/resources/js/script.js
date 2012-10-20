function initializePage() {
    var img = '	\
	<math xmlns="http://www.w3.org/1998/Math/MathML" display="block">	\
			  <mi>x</mi> <mo>=</mo>	\
			  <mrow>	\
				<mfrac>	\
				  <mrow>	\
					<mo>&#x2212;</mo>	\
					<mi>b</mi>	\
					<mo>&#x00B1;</mo>	\
					<msqrt>	\
					  <msup><mi>b</mi><mn>2</mn></msup>	\
					  <mo>&#x2212;</mo>	\
					  <mn>4</mn><mi>a</mi><mi>c</mi> \
					</msqrt> \
				  </mrow> \
				  <mrow> <mn>2</mn><mi>a</mi> </mrow> \
				</mfrac> \
			  </mrow> \
			  <mtext>.</mtext> \
			</math> \
	';

    $('.ajaxFocusPopover').popover({content:img, trigger:'manual', placement:'bottom'}).click(function (e) {
        $(this).popover('toggle');
        MathJax.Hub.Queue(["Typeset", MathJax.Hub]);
        e.preventDefault();
    });

    $('.context-word').each(function () {
        var self = $(this);
        var content = '<p>' + self.data('parse-result') + '</p>';
        content += '<button class="btn btn-primary">Go (' + self.data('word-id') + ')</button>';
        self.popover({content:content, trigger:'click', placement:'bottom'});
    });

    $('.context-sentence').each(function () {
        var self = $(this);
        var content = '<button class="btn btn-primary">Go (' + self.data('sentence-id') + ')</button>';
        self.popover({content:content, trigger:'click', placement:'bottom'});
    });
}