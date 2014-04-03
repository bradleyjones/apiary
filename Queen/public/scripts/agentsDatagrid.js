/*
 * Datagrid containing the list of agents
 *
 * __author__ = "Bradley Jones"
 * __credits__ = ["Bradley Jones", "Jack Fletcher", "John Davidge", "Sam Betts"]
 * __license__ = "Apache v2.0"
 * __version__ = "1.0"
 */

var StaticDataSource = function (options) {
  this._columns = options.columns;
  this._delay = options.delay || 0;
  this._data = options.data;
};

StaticDataSource.prototype = {

  columns: function () {
    return this._columns;
  },

  data: function (options, callback) {
    var self = this;

    setTimeout(function () {
      var data = $.extend(true, [], self._data);

      // SEARCHING
      if (options.search) {
        data = _.filter(data, function (item) {
          var match = false;

          _.each(item, function (prop) {
            if (_.isString(prop) || _.isFinite(prop)) {
              if (prop.toString().toLowerCase().indexOf(options.search.toLowerCase()) !== -1) match = true;
            }
          });

          return match;
        });
      }

      var count = data.length;

      // SORTING
      if (options.sortProperty) {
        data = _.sortBy(data, options.sortProperty);
        if (options.sortDirection === 'desc') data.reverse();
      } // SORT BY TIMESTAMP
      else {
        data = _.sortBy(data, 'TIMESTAMP');
        data.reverse();
      }


      // PAGING
      var startIndex = options.pageIndex * options.pageSize;
      var endIndex = startIndex + options.pageSize;
      var end = (endIndex > count) ? count : endIndex;
      var pages = Math.ceil(count / options.pageSize);
      var page = options.pageIndex + 1;
      var start = startIndex + 1;

      data = data.slice(startIndex, endIndex);

      console.log(data);
      for (var i = 0; i < data.length; i++) {
        var id = data[i].UUID;
        data[i].UUID = '<a onclick="testnewtarget(\''+id+'\')">'+id+'</a>';
      }

      callback({ data: data, start: start, end: end, count: count, pages: pages, page: page });

    }, this._delay)
  }
};

var dataSource = new StaticDataSource({
  columns: [
  {
    property: 'TIMESTAMP',
      label: 'Time Initiated',
      sortable: true
  },
  {
    property: 'UUID',
      label: 'UUID',
      sortable: true
  },
  {
    property: 'DEAD',
      label: 'Dead',
      sortable: true
  },
  {
    property: 'MACHINEID',
      label: 'Machine Hostname',
      sortable: true
  }],
  data:[],
  delay: 250
  });

$('#AgentsGrid').datagrid({
  dataSource: dataSource,
  stretchHeight: true
});
