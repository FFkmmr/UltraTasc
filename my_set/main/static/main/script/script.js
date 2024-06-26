
document.addEventListener('DOMContentLoaded', function() {
    const industryFilterInput = document.getElementById('industryFilter');
    const technologyFilterInput = document.getElementById('technologyFilter');
    const resetIndustryFilterBtn = document.getElementById('resetIndustryFilterBtn');
    const resetTechnologyFilterBtn = document.getElementById('resetTechnologyFilterBtn');
    const industryList = document.getElementById('industryList');
    const technologyList = document.getElementById('technologyList');
    const industryCheckboxes = document.querySelectorAll('.industry-checkbox');
    const technologyCheckboxes = document.querySelectorAll('.technology-checkbox');

    const industries = Array.from(industryList.getElementsByTagName('li'));
    const technologies = Array.from(technologyList.getElementsByTagName('li'));
    
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    resetFilter(industryFilterInput, industries);
    resetFilter(technologyFilterInput, technologies);
    function filterList(input, items) {
        const filterText = input.value.toLowerCase();
        items.forEach(item => {
            const label = item.querySelector('label');
            item.style.display = label.textContent.toLowerCase().includes(filterText) ? 'block' : 'none';
        });
    }
    function resetFilter(input, items) {
        if (input.tagName.toLowerCase() === 'input') {
            input.value = '';
        } else if (input.tagName.toLowerCase() === 'select') {
            input.selectedIndex = 0; 
        }
        
        items.forEach(item => {
            if (item.tagName.toLowerCase() === 'li') {
                const checkbox = item.querySelector('input[type="checkbox"]');
                if (checkbox) {
                    checkbox.checked = false;
                }
            }
            item.style.display = 'block'; 
        });
    }
    industryFilterInput.addEventListener('input', () => filterList(industryFilterInput, industries));
    technologyFilterInput.addEventListener('input', () => filterList(technologyFilterInput, technologies));
    resetIndustryFilterBtn.addEventListener('click', () => resetFilter(industryFilterInput, industries));
    resetTechnologyFilterBtn.addEventListener('click', () => resetFilter(technologyFilterInput, technologies));

    var privateButton = document.querySelector('.custom-btn[data-value="Private"]');
    if (privateButton) {
        privateButton.classList.add('active');
    }

    var buttons = document.querySelectorAll('.custom-btn');
    buttons.forEach(function(button) {
        button.addEventListener('click', function() {
            if (!this.classList.contains('active')) {
                buttons.forEach(function(btn) {
                    btn.classList.remove('active');
                });
                this.classList.add('active');
            }
        });
    });
    industryCheckboxes.forEach(checkbox => {
        checkbox.addEventListener('change', updateProjects);
    });
    technologyCheckboxes.forEach(checkbox => {
        checkbox.addEventListener('change', updateProjects);
    });

    function updateProjects() {
    const industryCheckboxes = document.querySelectorAll('.industry-checkbox');
    const technologyCheckboxes = document.querySelectorAll('.technology-checkbox');

    const selectedIndustries = Array.from(industryCheckboxes)
                                    .filter(checkbox => checkbox.checked)
                                    .map(checkbox => checkbox.value);
    const selectedTechnologies = Array.from(technologyCheckboxes)
                                      .filter(checkbox => checkbox.checked)
                                      .map(checkbox => checkbox.value);

    const projectListUrl = "/project_list/";         
    fetch(projectListUrl, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken'),
        },
        body: JSON.stringify({
            industries: selectedIndustries,
            technologies: selectedTechnologies
        }),
    })
    .then(response => response.json())
    .then(data => {
        const projectContainer = document.getElementById('projects');
        projectContainer.innerHTML = data.html;
    })
    .catch(error => console.error('Error:', error));
}

document.querySelectorAll('.industry-checkbox, .technology-checkbox').forEach(checkbox => {
    checkbox.addEventListener('change', updateProjects);
});

});
