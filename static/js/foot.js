  var tooltipTrigger = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
        var tooltipList = tooltipTrigger.map(function (El) {
            return new bootstrap.Tooltip(El)
        })