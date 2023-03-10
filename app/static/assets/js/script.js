async function makeRequestWithJWT() {
    const options = {
      method: 'post',
      credentials: 'same-origin',
      headers: {
        'X-CSRF-TOKEN': getCookie('csrf_access_token'),
      },
    };
    const response = await fetch('/insert', options);
    const result = await response.json();
    return result;
  }