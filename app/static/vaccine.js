document.addEventListener('DOMContentLoaded', function () {
  const vaccineSelect = document.getElementById('select-vaccine-1');
  const dosesSelect = document.getElementById('select-vaccine-counts-1');
  const vaccineEntry = document.getElementById("vaccine-entry");
  const birthdateInput = document.getElementById("birthdate");
  const vaccinationDateInput = document.getElementById("vaccination-date");
  let vaccines = {};
  let entryCount = 1;

  // JSONファイルを読み込み
  fetch(dataUrl)
  .then(response => {
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    return response.json();
  })
  .then(data => {
    vaccines = data;
    populateVaccineOptions(vaccines);  // ワクチンのオプションを生成
  })
  .catch(error => console.error('Error loading the JSON file:', error));

  // 接種日が変更されたとき、誕生日の最大日付を設定
  vaccinationDateInput.addEventListener('change', function() {
    const vaccinationDate = vaccinationDateInput.value;
    birthdateInput.setAttribute('max', vaccinationDate);
  });

  // ワクチンのオプションを生成
  function populateVaccineOptions(vaccineData) {
    Object.keys(vaccineData).forEach(vaccineName => {
      const option = document.createElement('option');
      option.value = vaccineName;
      option.textContent = `${vaccineName}`;
      vaccineSelect.appendChild(option);
    });
  }

  // ワクチン選択に応じて接種回数のドロップダウンを生成
  vaccineSelect.addEventListener('change', function () {
    updateDosesSelect(vaccineSelect, dosesSelect, vaccines);
  });

  function updateDosesSelect(vaccineSelectElement, dosesSelectElement, vaccinesData) {
    const selectedVaccine = vaccineSelectElement.value;
    dosesSelectElement.innerHTML = ''; // 接種回数のオプションをリセット
    dosesSelectElement.disabled = true;

    if (selectedVaccine !== 'none' && vaccinesData[selectedVaccine]) {
      const vaccineData = vaccinesData[selectedVaccine];
      for (let i = 1; i <= vaccineData['max-counts']; i++) {
        const option = document.createElement('option');
        option.value = i;
        option.textContent = i;
        dosesSelectElement.appendChild(option);
      }
      dosesSelectElement.disabled = false;  // 選択可能にする
    } else {
      dosesSelectElement.innerHTML = '<option value="none">ワクチンを選択してください</option>';
    }
  }

  // 新しいエントリーを追加し、イベントリスナーを設定
  document.getElementById("add-vaccine").addEventListener("click", function() {
    entryCount += 1
    const newEntry = vaccineEntry.cloneNode(true);
    const parent = document.getElementById("entries");
    newEntry.id = "vaccine-entry-" + entryCount;

    // クローンされたエントリーの中の要素を取得
    const newVaccineSelect = newEntry.querySelector(`#select-vaccine-1`);
    const newDosesSelect = newEntry.querySelector(`#select-vaccine-counts-1`);
    newVaccineSelect.id = 'select-vaccine-' + entryCount;
    newDosesSelect.id = 'select-vaccine-counts-' + entryCount;

    parent.appendChild(newEntry);

    // クローンされたエントリーにもイベントリスナーを設定
    newVaccineSelect.addEventListener('change', function () {
      updateDosesSelect(newVaccineSelect, newDosesSelect, vaccines);
    });
  });

  // フォームの非同期送信
  document.getElementById('vaccine-form').addEventListener('submit', function(event) {
    event.preventDefault(); // デフォルトのフォーム送信を防ぐ

    // ワクチンと回数のデータを取得するディクショナリを作成
    const vaccineData = {};
    const inputEntries = document.querySelectorAll('#select-vaccines .vaccine-row');
 
    inputEntries.forEach((inputEntry, index) => {
      const vaccineSelect = inputEntry.querySelector(`#select-vaccine-${index + 1}`).value;
      const dosesSelect = inputEntry.querySelector(`#select-vaccine-counts-${index + 1}`).value;
      if (vaccineSelect !== 'none' && dosesSelect !== 'none') {
        vaccineData[vaccineSelect] = dosesSelect;  // ワクチン名をキー、接種回数を値として格納
      }
    });


    // 送信用データを直接JSON形式で作成
    const bodyData = {
      "vaccination-date": vaccinationDateInput.value,
      "birthdate": birthdateInput.value,
      "vaccine_data": vaccineData
    };
    
    //受信したJSON（check_list）を処理する関数
      // チェックボックス生成関数
    function generateCheckListHTML(checkList) {
      let checklistHTML = '<label id=checklist-label><確認事項></label>';
      checkList.forEach((item, index) => {
        checklistHTML += `
          <div class="checklist-row">
            <input type="checkbox" id="check${index}" name="check${index}">
            <label for="check${index}">${item}</label>
          </div>
        `;
      });
      return checklistHTML;
    }

    function generateWarningListHTML(warningList){
      let warninglistHTML = '<label id=warning-label>>>> 注意 <<<</label>';
      warningList.forEach((item, index) => {
        warninglistHTML += `<p class="warning-message">${item}</p>`;
      });
      return warninglistHTML
    }

    function generateAttendTableHTML(attend_json) {
      let attendtableHTML = "\
              <label id='table-label'><次回接種案内></label>\
              <table border='1'><thead><tr><th>ワクチン名</th><th>回数</th><th>接種時期</th></tr></thead><tbody>";
      // JSONデータをループして、各行のHTMLを作成
      attend_json.forEach(function(item) {
          attendtableHTML += `<tr>
                                <td>${item["ワクチン名"]}</td>
                                <td>${item["回数"]}</td>
                                <td>${item["接種時期"]}</td>
                              </tr>`;
      });
      attendtableHTML += "</tbody></table>";
      return attendtableHTML;
  }


    // JSON形式で送信
    fetch('/submit', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(bodyData)  // ここでJSONに変換して送信
    })
    .then(response => response.json())
    .then(data => {
      if (data.error) {
        const resultDiv = document.getElementById('result');
        document.getElementById('result').innerHTML = `<p style="color: red; font-weight: bold;">${data.error}</p>`;
        resultDiv.style.display = 'flex';
      } else {
        const resultDiv = document.getElementById('result');

        // 表示するHTML要素
        const checkListContainer = document.getElementById('checklist-container');
        const warningListContainer = document.getElementById("warninglist-container");
        const attendTableContainer = document.getElementById("attendtable-container");

        checkListContainer.innerHTML = '';  // チェックリストコンテナをリセット
        warningListContainer.innerHTML = '';  // 警告リストコンテナをリセット
        attendTableContainer.innerHTML = '';  // 接種スケジュールコンテナをリセット

        // 要素生成関数を呼び出す
        const checkListHTML = generateCheckListHTML(data.check_list);
        const warningListHTML = generateWarningListHTML(data.warning_list);
        const attendTableHTML = generateAttendTableHTML(data.attend_json);

        // check_listが存在する場合のみ表示
        if (data.check_list && data.check_list.length > 0) {
          checkListContainer.innerHTML += checkListHTML;
          checkListContainer.style.display = 'block'; // データがある場合は表示
        } else {
          checkListContainer.style.display = 'none'; // 非表示

        }

        // warning_listが存在する場合のみ表示
        if (data.warning_list && data.warning_list.length > 0) {
          warningListContainer.innerHTML += warningListHTML;
          warningListContainer.style.display = 'block'; // データがある場合は表示
        } else {
          warningListContainer.style.display = "none";
        }

        // attend_jsonが存在する場合のみ表示
        if (data.attend_json && data.attend_json.length > 0) {
          attendTableContainer.innerHTML += attendTableHTML;
          attendTableContainer.style.display = 'block'; // データがある場合は表示
        } else {
          attendTableContainer.style.display = "none";
        }

        resultDiv.style.display = "block";



      }
    })
    .catch(error => {
      const resultDiv = document.getElementById('result'); 
      document.getElementById('result').innerHTML = `<p style="color: red; font-weight:bold;">エラーが発生しました。リロードしてやり直してください。</p>`;
      resultDiv.style.display = 'flex';

    });
  });
});