import { api } from './Auth';

export const FileAPI = {
    async getFileTypes() {
        const { data } = await api.get('/file/types');
        return data.allowed_file_types;
    },

    async uploadFiles(files: File[]) {
        const formData = new FormData();
        files.forEach(file => {
            formData.append('files', file);
        });

        const { data } = await api.post('/file/upload', formData, {
            headers: {
                'Content-Type': 'multipart/form-data',
            },
        });
        return data;
    }
};

