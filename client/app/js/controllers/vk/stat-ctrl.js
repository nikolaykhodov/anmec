angular.module('vk').controller("vkStatController", function($scope, $routeParams, $location, vkApi, anmecApi, $q, modal) {

  $scope.statIsLoading = true;
  $scope.likeStatIsLoading = true;

  function groupInfoLoaded(results) {
    console.log(results);
    var groups = results[0];
    var wall = results[1];
    var group = groups[0];

    $scope.groupName = group.name;
    $scope.members = group.members_count;
    $scope.posts = wall[0];
  }

  function processStats(stats) {
    var labels = [], 
        visitors = [], 
        reach = [], 
        reachSubscribers = [], 
        views = [];
    var sex = {},
        age= {};

    stats.forEach(function(el) {
      labels.push(el.day);
      visitors.push(el.visitors);
      views.push(el.views);
      reach.push(el.reach ? el.reach : 0);
      reachSubscribers.push(el.reach_subscribers ? el.reach_subscribers : 0);
      //подсчет распределения по полу
      if (el.sex) el.sex.forEach(function (sx) {
        if (sex[sx.value])
          sex[sx.value] += sx.visitors;
        else
          sex[sx.value] = sx.visitors;
      });
      //подсчет распределения по возрасту
      if (el.age) el.age.forEach(function (ag) {
        if (age[ag.value]) {
          age[ag.value] += ag.visitors;
        } else {
          age[ag.value] = ag.visitors;
        }
      });
    });

    return {
      labels: labels,
      visitors: visitors,
      reach: reach,
      reachSubscribers: reachSubscribers,
      views: views,
      sex: sex,
      age: age
    };
  }

  function drawMainChart(labels, views, visitors, reach, reachSubscribers) {
    var viewsLine = [],
        visitorsLine=[],
        reachLine=[],
        reachSubscribersLine=[];

    for (var i = 0; i < labels.length; i++) {
      viewsLine.push([[labels[i]], views[i]]);
      visitorsLine.push([[labels[i]], visitors[i]]);
      reachLine.push([[labels[i]], reach[i]]);
      reachSubscribers.push([[labels[i]], reachSubscribers[i]]);
    }

    $scope.mainChartData = [viewsLine, visitorsLine, reachLine, reachSubscribersLine];

    $scope.mainChartParams = {
      animate: true,
      axes: {
        xaxis: {
          renderer: $.jqplot.DateAxisRenderer
        }
      },
      series: [{ label: 'Просмотры' }, { label: 'Посетители' }, { label: 'Охват' }, { label: 'Охват подписчиков' }],
      legend: {
        renderer: $.jqplot.EnhancedLegendRenderer,
        show: true, 
        location: 's', 
        rendererOptions: {
          numberRows: 1,
          marginLeft: 40
        }
      }
    };
  }

  function getSmallChartParams(rows) {
    return  {
      seriesDefaults: {
        renderer: $.jqplot.PieRenderer,
        rendererOptions: {
          showDataLabels: true
        }
      },
      highlighter: {
        sizeAdjust: 10,
        tooltipLocation: 'n',
        tooltipAxes: 'xy',
        tooltipFormatString: '%s',
        tooltipSeparator: ': ',
        useAxesFormatters: false
      },
      legend: {
        renderer: $.jqplot.EnhancedLegendRenderer,
        show: true, 
        location: 's', 
        rendererOptions: {
          numberRows: rows,
          marginLeft: 40
        }
      }
    };
  }

  function drawSexChart(sex) {
    var data = [['Мужчины', sex.m], ['Женщины', sex.f]];

    $scope.sexChartData = [data];
    $scope.sexChartParams = getSmallChartParams(1);
  }

  function drawAgeChart(ages) {
    var data = [];
    for (var age in ages) {
      data.push([age, ages[age]]);
    }

    $scope.ageChartData = [data];
    $scope.ageChartParams = getSmallChartParams(2);
  }

  function statsLoaded(stats) {
    var data = processStats(stats);

    drawMainChart(data.labels, data.views, data.visitors, data.reach, data.reachSubscribers);
    drawSexChart(data.sex);
    drawAgeChart(data.age);

    $scope.statIsLoading = false;
  }

  function processLikeStats(stats) {
    var postsStatistics = [];

    stats.posts.forEach(function(part) {
      for (var i = 1; i < part[0].length; i++) {
        var post = {
          id: part[0][i],
          time: new Date(1000 * part[1][i]).getHours(),
          likes: part[2][i],
          reposts: part[3][i],
          comments: part[4][i],
        };
        
        if (postsStatistics[post.time]) {
          postsStatistics[post.time].posts++;
          postsStatistics[post.time].comments += post.comments;
          postsStatistics[post.time].likes += post.likes;
          postsStatistics[post.time].reposts += post.reposts;
        } else 
          postsStatistics[post.time] = {
            posts: 1,
            comments : post.comments,
            likes : post.likes,
            reposts : post.reposts
          };
        
      }
    });

    return postsStatistics;
  }

  function computeLikesChartData(statistics) {
    var likesLine = [], 
        postsLine = [], 
        commentsLine = [], 
        repostsLine = [];

    for (var time in statistics) {
      likesLine.push([time, statistics[time].likes]);
      commentsLine.push([time, statistics[time].comments]);
      repostsLine.push([time, statistics[time].reposts]);
    }
    return [likesLine, commentsLine, repostsLine]
  }

  function drawLikeStats(stats) {

    $scope.likesChartParams = {
      animate: true,
      axes: {
        xaxis: {
          min: 0,
          max: 24
        }
      },
      series: [{ label: 'Лайки' }, { label: 'Комментарии' }, { label: 'Репосты' }],
      legend: {
        renderer: $.jqplot.EnhancedLegendRenderer,
        show: true, location: 's', rendererOptions: {
          numberRows: 1,
          marginLeft: 40
        }
      }
    };

    $scope.likesChartData = computeLikesChartData(
      processLikeStats(stats)
    );
  }

  function likeStatsLoaded(stats) {
    $scope.likeStatIsLoading = false;
    drawLikeStats(stats);
  }

  try {
    $scope.mids = $routeParams.query.split(',').
    filter(function(mid) {
      mid = parseInt(mid);
      return isNaN(mid) === false && mid !== 0;
    }).map(function(mid) {
      return parseInt(mid);
    });
    $scope.groupId = $scope.mids[0];
  } catch(e) {
    $scope.groupId = 0;
  }

  if($scope.groupId === 0) {
    modal.alertDialog($scope, 'Ошибка', 'Вам необходимо указать группу');
  } else {
    $scope.groupName = '#' + $scope.groupId;

    var promises = $q.all([
      vkApi.request('groups.getById', {group_id: $scope.groupId, fields: 'members_count'}),
      vkApi.request('wall.get', {owner_id: -$scope.groupId})
    ]);

    promises.then(
      groupInfoLoaded,
      function(reason) {
        modal.alertDialog($scope, 'Ошибка', reason);
      }
    );

    vkApi.getStats($scope.groupId, 30).then(
      statsLoaded,
      function(reason) {
        modal.alertDialog($scope, 'Ошибка', reason);
      }
    );
    vkApi.getLikeStats($scope.groupId, 30).then(
      likeStatsLoaded,
      function(reason) {
        modal.alertDialog($scope, 'Ошибка', reason);
      }
    );
}


});
