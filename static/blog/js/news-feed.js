  $(function () {
            var end_date = new Date();
            var $window = $(window);
            var $document = $(document);
            var $news_feed = $('#news-feed');

            function bind() {
                $window.scroll(function () {
                    if($window.scrollTop() + $window.height() > $document.height() - 200) {
                        ajaxRequest(bind);
                        $window.unbind('scroll');
                    }
                })
            }

            function createFeed(data) {
                var flag = true;
                data['value'].forEach(function (value) {
                    if (value['type'] == 1) {
                        $news_feed.append(
                                $('<div>').attr('class', 'timelabel').append(
                                        $('<span>').attr('class', 'bg-gray').append(value['date'])
                                ));
                    }
                    else if (value['type'] == 2) {
                        $news_feed.append(
                                $('<div>').attr('class', 'col-md-6 col-sm-6 col-xs-12').append(
                                        $('<i>').attr('class', value['class'])
                                ).append(
                                        $('<div>').attr('class', 'timeline-item').append(
                                                $('<span>').attr('class', 'time').append(
                                                        $('<i>').attr('class', 'fa fa-clock-o').append(' ' + value['time'])
                                                )
                                        ).append(
                                                $('<div>').attr('class', 'timeline-header').append(
                                                        $('<div>').attr('class', 'btn-group').append(
                                                                $('<a>').attr('class', 'btn btn-default btn-xs')
                                                                        .attr('href', '/condominium/'+value['town_slug']+'/home')
                                                                        .append(value['town_name'])
                                                        ).append(
                                                                $('<a>').attr('class', 'btn btn-default btn-xs')
                                                                        .attr('href', '/condominium/'+value['town_slug']+'/' + value['module_link'])
                                                                        .append(value['module_name'])
                                                        )
                                                )
                                        ).append(
                                                $('<div>').attr('class', 'timeline-body').attr('style', 'overflow: auto')
                                                        .append(
                                                                $('<div>').append(
                                                                        $('<a>').attr('href', '/condominium/'+value['town_slug']+'/' + value['module_link'] + value['id']).append(
                                                                                $('<img>').attr('src', value['image'] || '/static/img/empty.gif').attr('class', 'margin')
                                                                                        .attr('style', 'max-width: 100%; max-height: 100%;')
                                                                                        .error(function () {
                                                                                            $(this).attr('src', '/static/img/empty.gif')
                                                                                        })
                                                                        )
                                                                )
                                                        ).append(
                                                                $('<div>').append(
                                                                        $('<p>').attr('style', 'font-size: 14px').append(value['status'])
                                                                ).append(
                                                                        $('<a>').attr('href', '/condominium/'+value['town_slug']+'/' + value['module_link'] + value['id'])
                                                                                .attr('style', 'font-size: 18px;')
                                                                                .append(value['header'])
                                                                ).append(
                                                                        $('<p>').append(
                                                                                $('<small>').append(value['content'])
                                                                        )

                                                )
                                                )
                                        )

                                )
                        )
                    } else {
                        /*No more news*/
                        flag = false;
                    }
                });

                end_date = new Date(data['end_date']);
                if (flag) bind();
                else {
                    console.log('Unbinded');
                    $news_feed.append(
                            $('<li>').attr('class', 'time-label').append(
                                    $('<span>').attr('class', 'bg-red').append('Схоже ви досягли останніх подій.\n Далі шляху немає')
                            )
                    )
                }

                $('#image').remove()
            }

            function ajaxRequest() {
                $news_feed.append('<div id="image" class="text-center"><i class="fa fa-refresh fa-spin" style="font-size: 65px; color: #00733e"></i></div>');
                $.ajax({
                    url: '/index/lastnews',
                    type: 'GET',
                    dataType: 'json',
                    data: {
                        "date": end_date.toJSON()
                    },
                    success: function (response) {
                        createFeed(response);
                    }
                })
            }

            $document.ready(function () {
                ajaxRequest();
            });

        });