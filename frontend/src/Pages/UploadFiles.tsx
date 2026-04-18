import { useEffect, useState, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import { useDropzone } from 'react-dropzone';
import {
    Box,
    Button,
    Card,
    CardContent,
    CircularProgress,
    Dialog,
    DialogActions,
    DialogContent,
    DialogContentText,
    DialogTitle,
    List,
    ListItem,
    ListItemText,
    Typography,
    Alert,
    Snackbar
} from '@mui/material';
import { FileAPI } from '../API/FileAPI';

export default function UploadFiles() {
    const navigate = useNavigate();
    const [allowedExtensions, setAllowedExtensions] = useState<string[]>([]);
    const [files, setFiles] = useState<File[]>([]);
    const [loading, setLoading] = useState(false);

    // Popup states
    const [cancelDialogOpen, setCancelDialogOpen] = useState(false);
    const [successDialogOpen, setSuccessDialogOpen] = useState(false);
    const [errorMsg, setErrorMsg] = useState('');

    useEffect(() => {
        FileAPI.getFileTypes()
            .then(types => setAllowedExtensions(types || []))
            .catch(err => console.error("Could not fetch file types:", err));
    }, []);

    // Create a react-dropzone accept object
    const acceptMap: Record<string, string[]> = {};
    allowedExtensions.forEach(ext => {
        const lowerExt = ext.toLowerCase();
        // Since we don't have mime types, we rely on extensions
        // Using a generic catch-all mime to map to extensions
        if (!acceptMap['*/*']) {
            acceptMap['*/*'] = [];
        }
        acceptMap['*/*'].push(`.${lowerExt}`);
    });

    const onDrop = useCallback((acceptedFiles: File[]) => {
        setFiles(prev => [...prev, ...acceptedFiles]);
    }, []);

    const { getRootProps, getInputProps, isDragActive } = useDropzone({
        onDrop,
        accept: Object.keys(acceptMap).length > 0 ? acceptMap : undefined,
    });

    const handleRemoveFile = (index: number) => {
        setFiles(prev => prev.filter((_, i) => i !== index));
    };

    const handleCancelClick = () => {
        if (files.length > 0) {
            setCancelDialogOpen(true);
        } else {
            navigate('/');
        }
    };

    const confirmCancel = () => {
        setCancelDialogOpen(false);
        navigate('/');
    };

    const handleSubmit = async () => {
        if (files.length === 0) return;
        setLoading(true);
        setErrorMsg('');

        try {
            await FileAPI.uploadFiles(files);
            setSuccessDialogOpen(true);
        } catch (error: any) {
            const msg = error.response?.data?.error || "Error uploading files";
            setErrorMsg(msg);
        } finally {
            setLoading(false);
        }
    };

    const handleSuccessOk = () => {
        setSuccessDialogOpen(false);
        navigate('/');
    };

    return (
        <Box sx={{ p: 4, maxWidth: 800, margin: '0 auto' }}>
            <Typography variant="h4" gutterBottom>
                Upload Files
            </Typography>

            {allowedExtensions.length > 0 && (
                <Typography variant="body2" color="textSecondary" sx={{ mb: 2 }}>
                    Allowed file types: {allowedExtensions.join(', ')}
                </Typography>
            )}

            {files.length > 0 && (
                <Card sx={{ mb: 3 }}>
                    <CardContent>
                        <Typography variant="h6">Selected Files</Typography>
                        <List>
                            {files.map((file, index) => (
                                <ListItem
                                    key={`${file.name}-${index}`}
                                    secondaryAction={
                                        <Button color="error" onClick={() => handleRemoveFile(index)} disabled={loading}>
                                            Remove
                                        </Button>
                                    }
                                >
                                    <ListItemText primary={file.name} secondary={`${(file.size / 1024).toFixed(2)} KB`} />
                                </ListItem>
                            ))}
                        </List>
                    </CardContent>
                </Card>
            )}

            <Card
                {...getRootProps()}
                sx={{
                    mb: 3,
                    p: 4,
                    border: '2px dashed',
                    borderColor: 'primary.main',
                    backgroundColor: isDragActive ? '#e3f2fd' : '#fafafa',
                    cursor: 'pointer',
                    textAlign: 'center'
                }}
            >
                <input {...getInputProps()} />
                {isDragActive ? (
                    <Typography>Drop the files here ...</Typography>
                ) : (
                    <Typography>
                        Drag & drop some files here, or click to select files
                    </Typography>
                )}
            </Card>

            <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
                <Button variant="outlined" color="error" onClick={handleCancelClick} disabled={loading}>
                    Cancel
                </Button>
                <Button variant="contained" color="primary" onClick={handleSubmit} disabled={files.length === 0 || loading}>
                    {loading ? <CircularProgress size={24} color="inherit" /> : 'Submit'}
                </Button>
            </Box>

            {/* Cancel Confirmation Dialog */}
            <Dialog open={cancelDialogOpen} onClose={() => setCancelDialogOpen(false)}>
                <DialogTitle>Confirm Cancel</DialogTitle>
                <DialogContent>
                    <DialogContentText>
                        You have selected files. Are you sure you want to cancel and go back? You will lose these selections.
                    </DialogContentText>
                </DialogContent>
                <DialogActions>
                    <Button onClick={() => setCancelDialogOpen(false)}>No</Button>
                    <Button onClick={confirmCancel} color="error" autoFocus>
                        Yes, Cancel
                    </Button>
                </DialogActions>
            </Dialog>

            {/* Success Notification Dialog */}
            <Dialog open={successDialogOpen} onClose={handleSuccessOk}>
                <DialogTitle>Success</DialogTitle>
                <DialogContent>
                    <DialogContentText>
                        Your files have been uploaded and will be processed shortly.
                    </DialogContentText>
                </DialogContent>
                <DialogActions>
                    <Button onClick={handleSuccessOk} color="primary" variant="contained">
                        OK
                    </Button>
                </DialogActions>
            </Dialog>

            {/* Error Snackbar */}
            <Snackbar
                open={!!errorMsg}
                autoHideDuration={6000}
                onClose={() => setErrorMsg('')}
                anchorOrigin={{ vertical: 'bottom', horizontal: 'center' }}
            >
                <Alert onClose={() => setErrorMsg('')} severity="error" sx={{ width: '100%' }}>
                    {errorMsg}
                </Alert>
            </Snackbar>
        </Box>
    );
}
